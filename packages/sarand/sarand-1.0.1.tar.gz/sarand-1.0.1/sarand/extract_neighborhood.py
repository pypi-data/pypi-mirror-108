"""
File:		extract_neighborhood.py
Aythor:		Somayeh Kafaie
Date:		July 2020
Purpose:	To extract the neighborhood of an AMR gene from an assembly graph

To run:
- The Bandage+BLAST implementation:
	python extract_neighborhood.py --amr/-A <AMR gene file path in FASTA format>
	--gfa/-G <GFA assembly graph> --distance/-D <max distance from AMR gene (default=1)>
	--length/-L <length of the linear sequence around AMR gene to be extracted (default = 1000)>

"""

################################################################################

import sys
import os
import errno
import gfapy
import re
import argparse
import difflib
import datetime
import csv
import collections
from Bio import SeqIO
from gfapy.sequence import rc
import shutil
import logging
import enum

from utils import reverse_sign, find_node_orient, find_node_name, find_node_name_orient,\
					exist_in_path, compare_two_sequences, read_path_info_from_align_file,\
					create_fasta_file
from params import Assembler_name
#from find_seq_in_contigs import find_sequence_match

BANDAGE_PATH = '/media/Data/tools/Bandage_Ubuntu_dynamic_v0_8_1/Bandage'
OUT_DIR = 'output/'
BOTH_DIR_RECURSIVE = True
#MAX_K_MER_SIZE = 55
#if this feature is true after that the extracted length reaches a threshold, we don't go
#over all edges in the neighbourhood (in pre_sequence and post_sequence extraction)
#and only extract the sequence from the longest one to reduce the processing time!!!
ONLY_LONGEST_EDGE = False
TEMP_DIR = 'temp/'

def retrieve_AMR(file_path):
	"""
	To read the AMR gene from the fasta file.
	Parameters:
		file_path:	the address of the file containing the AMR gene
	Return:
		the sequence of the AMR gene in lower case
	"""
	with open(file_path) as fp:
		for line in fp:
			if line.startswith('>'):
				continue
			return line.lower()

def similar_sequence_exits(seq_list, query_seq, output_dir):
	"""
	To check if any similar sequence to query_seq exists in seq_list
	if it finds any similar one with a shorter length, replaces that with query_Seq
	Parameters:
		seq_list: 	the list of sequences
		query_seq:	the query sequence
		output_dir:	the output directory
	Return:
		the index of the similar seq if it has a shorter length than query_seq (to be replace)
		and
		True if a seq similar to query_seq was found in seq_list

	"""
	for i, seq in enumerate(seq_list):
		if compare_two_sequences(seq, query_seq, output_dir, blast_ext = str(i)):
			#if the new sequence has a longer length replace the shorter similar oe with it
			if len(seq)<len(query_seq):
				return i, True
			else:
				return -1, True
	return -1, False

def find_sequence_match(query, contig_file, out_dir = TEMP_DIR, blast_ext = '',
						threshold =95, max_target_seqs = 100):
	"""
	To check if the sequence (query) can be found in the list of contigs
	# contig_file is considered our database and we run blast over it
	Parameters:
		query: the sequence we look for in the contigs
		contig_file: the file containing contigs
		out_dir: the output directory to store all created files there
		blast_ext: an extension used for naming blast file
	Return:
		the list of matched contigs and some further information including identity,
		matched_length, the start and end of matched part of the query, and the start
		and end of matched part of the contig
	"""
	# #Create DB from contig file
	# command = 'makeblastdb -in '+contig_file +' -parse_seqids -dbtype nucl'
	# os.system(command)
	#write the sequence into a fasta file
	query_file = out_dir+'/query.fasta'
	file = open(query_file, 'w')
	file.write(query)
	file.close()
	#run blast query for alignement
	blast_file_name = out_dir+'/blast'+blast_ext+'.csv'
	command = 'blastn -query '+query_file+' -db '+contig_file+\
		' -outfmt 10 -max_target_seqs '+str(max_target_seqs)+' -evalue 0.5 -perc_identity '+str(threshold-1)+' > '+ blast_file_name
	# command = 'blastn -query '+query_file+' -db '+contig_file+\
	# 	' -task blastn -outfmt 10 -max_target_seqs '+str(max_target_seqs)+' -evalue 0.5 -perc_identity '+str(threshold-1)+' > '+ blast_file_name
	# command = 'blastn -query '+query_file+' -db '+contig_file+\
	# 	' -task blastn -outfmt 10 -max_target_seqs 5 -evalue 0.5 -perc_identity 95 > '+ blast_file_name

	os.system(command)
	contig_list = []
	contig = collections.namedtuple('contig', 'name identity matched_length q_start q_end c_start c_end')
	with open(blast_file_name, 'r') as file1:
		myfile = csv.reader(file1)
		for row in myfile:
			mycontig = contig(name=row[1], identity=row[2], matched_length=row[3], q_start=row[6],
		 					q_end=row[7], c_start=row[8], c_end=row[9])
			contig_list.append(mycontig)

	return contig_list

def extract_amr_neighborhood_in_ref_genome(amr_seq, ref_path, neighborhood_len, threshold = 95):
	"""
	To find the neighborhood of amr_seq in the genome (ref_path)
	Parameters:
		amr_seq:	the sequence of the AMR gene
		ref_path:	the address of the reference genome
		neighborhood_len: 	the length of neighborhood from each side to be extracted
		threshold: used for identity and coverage
	Return:
		the neighborhood(s) of amr_seq with maximum length = 2*len + length(amr_seq)
			and the start position of the AMR in the extracted sequence(s)
	# In case AMR exists in multiple locations of the genome this function returns
		multiple neighborhood sequences
	"""
	# copy ref_path in a new temp location and folder that can be deleted at the end
	temp_dir = 'tmp_ref_path'
	if not os.path.exists(temp_dir):
		try:
			os.makedirs(temp_dir)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
			pass
	# tmp_path = temp_dir + '/'+os.path.basename(ref_path)
	# shutil.copyfile(ref_path, tmp_path)

	# check if the sequence can be found in the genome
	#record_list = find_sequence_match(amr_seq, tmp_path, temp_dir, threshold = threshold)
	record_list = find_sequence_match(amr_seq, ref_path, temp_dir, threshold = threshold)

	# to get ride of \n
	len_amr_seq = len(amr_seq)-1

	# read record_list and store cases with identity and coverage above the threshold
	# and extract the beginning and end of AMR in the ref_file
	found = False
	amr_start_list = []
	amr_end_list = []
	record_name_list = []
	# find the start and end of AMR for all found cases above the threshold
	for record in record_list:
		if int(float(record.identity))>=threshold and int(float(record.matched_length)/len_amr_seq*100)>=threshold:
			found = True
			amr_start_list.append(int(record.c_start))
			amr_end_list.append(int(record.c_end))
			record_name_list.append(record.name)

	# extract neighborhood sequence(s)
	seq_list = []
	contig_name_list = []
	if found:
		for i, amr_start in enumerate(amr_start_list):
			amr_end = amr_end_list[i]
			record_name = record_name_list[i]
			seq = ''
			reverse_complement = False
			# extract sequence from both sides
			if amr_start > amr_end:
				amr_start, amr_end = amr_end, amr_start
				reverse_complement = True
			for record in SeqIO.parse(open(ref_path,'r'),'fasta'):
				#if record.id == record_name:
				if record_name == record.id:
					amr_start = amr_start -1
					if amr_start-neighborhood_len >= 0:
						#seq = str(record.seq[amr_start-neighborhood_len:amr_end])
						seq = str(record.seq[amr_start-neighborhood_len:amr_start]).upper()+str(record.seq[amr_start:amr_end]).lower()
						amr_start = neighborhood_len
					else:
						#seq = str(record.seq[:amr_end])
						seq = str(record.seq[:amr_start]).upper()+str(record.seq[amr_start:amr_end]).lower()
					if (amr_end-1+neighborhood_len)<=len(record):
						seq+=str(record.seq[amr_end:amr_end+neighborhood_len])
					else:
						seq+=str(record.seq[amr_end:])
					if reverse_complement:
						seq = rc(seq)
					seq_list.append(seq)
					contig_name_list.append(record_name)
					break

	# delete the temp folder
	if os.path.exists(temp_dir):
		try:
			shutil.rmtree(temp_dir)
		except OSError as e:
			logging.error("Error: %s - %s." % (e.filename, e.strerror))
	#added by 1 because the index starts from 0 in the string
	return seq_list, contig_name_list

def extract_neighbourhood(segment, segment_list, edge_list, distance):
	"""
	To extract the neighbourghood of a node
	Parameters:
		segment: the node we are looking for its neighborhood
		segment_list: the list of segments in the neighbourhood so far
		edge_list: the list of edges in the neighbourhood so far
		distance: the maximum distance of neighbourhood we are going to extract from AMR gene
	Return:
		updated edge_list and segment_list
	"""
	if distance <= 0:
		return segment_list, edge_list
	for link in reversed(segment.dovetails_L):
		if link.from_segment.name != segment.name:
			other_side = link.from_segment
		elif link.to_segment.name != segment.name:
			other_side = link.to_segment
		else:
			logging.info("WARNING: the link is a loop for node#"+segment.name)
			other_side = segment
		if link not in edge_list:
			edge_list.append(link)
		segment_list.add(other_side.name)
		segment_list, edge_list =\
			extract_neighbourhood(other_side, segment_list, edge_list, distance - 1)
	for link in reversed(segment.dovetails_R):
		if link.from_segment.name != segment.name:
			other_side = link.from_segment
		elif link.to_segment.name != segment.name:
			other_side = link.to_segment
		else:
			logging.info("WARNING: the link is a loop for node#"+segment.name)
			other_side = segment
		if link not in edge_list:
			edge_list.append(link)
		segment_list.add(other_side.name)
		segment_list, edge_list =\
			extract_neighbourhood(other_side, segment_list, edge_list, distance - 1)
	return segment_list, edge_list

def create_graph(myGraph, segment_list, edge_list):
	"""
	To create a graph from the list of segments and edges
	Parameters:
		myGraph: The original graph (the new graph is a subgraph of this graph)
		segment_list: the list of segments of the new graph
		edge_list: the list of edges of the new graph
	Return:
		the created graph which is a subgraph of myGraph
	"""
	subGraph = gfapy.Gfa(version='gfa1')
	for segment_name in segment_list:
		seg = myGraph.segment(segment_name)
		seg.disconnect()
		subGraph.append(seg)
	for edge in edge_list:
		if edge.is_connected():
			edge.disconnect()
		subGraph.append(edge)
	return subGraph

def extract_subgraph(nodes, distance, file_path):
	"""
	To extract the neighborhood.
	This function calls the recursive function "extract_neighbourhood"
	for the first and last nodes in the path to do the job
	Parameters:
		nodes: the list of nodes we are interested in their neighbourhood
		distance: the maximum distance of neighbourhood we are going to extract from AMR gene
		file_path: the address of the original assembly graph in GFA format
	Return:
		the subgraph representing the neighbourhood of the node_lists in a given max distance
	"""
	myGraph = gfapy.Gfa.from_file(file_path)
	segment_list=set()
	edge_list = []
	#for now we just find the neighborhood of the first and last nodes in the path
	#Add first node in AMR path and find its neighborhood
	s = myGraph.segment(re.sub('[+-]', '', nodes[0]))
	segment_list.add(s.name)
	segment_list, edge_list = extract_neighbourhood(s, segment_list, edge_list, distance)
	#Add last node in AMR path and find its neighborhood
	if (len(nodes) > 1):
		segment_list_last = set()
		edge_list_last = []
		s = myGraph.segment(re.sub('[+-]', '', nodes[-1]))
		segment_list.add(s.name)
		segment_list_last, edge_list_last = extract_neighbourhood(s, segment_list_last, edge_list_last, distance)
		#merge the lists
		segment_list = segment_list.union(segment_list_last)
		for edge in edge_list_last:
			if edge not in edge_list:
				edge_list.append(edge)

	return myGraph, segment_list, edge_list

def write_sequences_to_file(sequence_list, path_list, file_name):
	"""
	To write the extracted sequences and paths in neighborhood of the AMR gene in a file
	Parameters:
		sequence_list: the list of sequences extracted in AMR gene neighborhood
		path_list: the list of all paths (a list of nodes) in AMR gene neighborhood
		file_name: the name of file to be writtn in
	"""
	file = open(file_name, 'a+')
	for seq, path in zip(sequence_list, path_list):
		myLine = "Path-> " + ", ".join(path) + ":"
		file.write(myLine+"\n")
		file.write(seq+"\n")
	file.close()

def sequence_on_orientation(seq, orient):
	"""
	To	return the sequence based on the orientation used in the graph
	Parameters:
	 	orient:	+ / -
		seq:	the original sequence
	Return: reverse complement for -; otherwise seq itself
		for orient = '-' and seq = 'AACTG' -> 'CAGTT'
	"""
	if orient=='-':
			return rc(seq)
	else:
		return seq

def find_overlap(from_node, to_node, from_orient, to_orient, validate_overlap_size = True):
	"""
	To return the size of overlap beween  from_node and to_node
	e.g.; from_node = 2, to_node = 3, from_orient = +, to_orient= +, edge = [L 2 + 3 + 55M]
				---->  return 55
	Parameters:
		from_node:	the first node of the edge
		to_node:	the second node of the edge
		from_orient:the orientation of the first node of the edge
		to_orient:	the orientation of the second node of the edge
		validate_overlap_size: to verify if the extracted size for overlap is correct and matches
	Return:
		the size of overlap
	"""
	size = 0
	for edge in (from_node.dovetails_L + from_node.dovetails_R):
		# 3561+ --> 15082+
		if edge.from_segment == from_node and edge.to_segment == to_node and\
			edge.from_orient == from_orient and edge.to_orient == to_orient:
			if edge.overlap[0].code == 'M':
				size = edge.overlap[0].length
				if (size>0 and validate_overlap_size):
					seq1 = sequence_on_orientation(edge.from_segment.sequence, edge.from_orient)
					seq2 = sequence_on_orientation(edge.to_segment.sequence, edge.to_orient)
					if seq1[len(seq1)-size:] != seq2[:size]:
						logging.info("WARNING: the overlap doesn't match: "+str(edge))
						logging.info("first sequence: "+seq1)
						logging.info("second sequence: "+seq2)
			else:
				logging.info("WARNING: the sequence from node "+from_node.name+" to node "+
						to_node.name + "has "+ edge.overlap[0] + " instead of overlap!")
			return size
		#sometimes we have the reverse complement of the edge and not itself
		# 15082- --> 3561-
		elif edge.from_segment == to_node and edge.to_segment == from_node and\
			edge.from_orient == reverse_sign(to_orient) and edge.to_orient == reverse_sign(from_orient):
			if edge.overlap[0].code == 'M':
				size = edge.overlap[0].length
				if (validate_overlap_size):
					seq1 = sequence_on_orientation(edge.to_segment.sequence, reverse_sign(edge.to_orient))
					seq2 = sequence_on_orientation(edge.from_segment.sequence, reverse_sign(edge.from_orient))
					if seq1[len(seq1)-size:] != seq2[:size]:
						logging.info("WARNING: the overlap doesn't match: "+str(edge))
						logging.info("first sequence: "+seq1)
						logging.info("second sequence: "+seq2)
			else:
				logging.info("WARNING: the sequence from node "+from_node.name+" to node "+
						to_node.name + "has "+ edge.overlap[0] + " instead of overlap!")
			return size
	return size

def remove_identical_sub_sequences(sequence_list, path_list):
	"""
	To keep only one instance in case of multiple identical extracted sequences or
	when a sequence is a subsequence of another one
	Parameters:
		sequence_list:	list of extracted sequences
		path_list:		list of extracted paths
	Return sequence_list and path_list in which every sequence/path is unique and
		none of them is subssequence/subpath of another one
	"""
	#In case two sequences are identical keep the one with the lower index in the list
	identical_sub_set = set()
	for i, seq1 in enumerate(sequence_list):
		for j, seq2 in enumerate(sequence_list):
			if i < j:
				if seq1==seq2 or seq2 in seq1:
					identical_sub_set.add(j)
				elif seq1 in seq2:
					identical_sub_set.add(i)

	identical_sub_list = sorted(identical_sub_set)
	for index in reversed(identical_sub_list):
		del sequence_list[index]
		del path_list[index]

	return sequence_list, path_list

def reverse_path(path):
	"""
	To generate the reverse of a path;
		e.g., [1+, [8-, 12+], 9-] --> [9+, [12-, 8+,] 1-]
	"""
	mypath = []
	items = ['[', ']', '{', '}']
	reversed_items = [']', '[', '}', '{']
	for node in reversed(path):
		mynode = ''
		num=''
		for ch in node:
			if ch in items:
				mynode = reversed_items[items.index(ch)] + mynode
			elif ch=='-' or ch=='+':
				num+=reverse_sign(ch)
				mynode = num + mynode
			else:
				num+=ch
		mypath.append(mynode)
	return mypath

def extract_found_amr(myGraph, node_list, orientation_list, start_pos, end_pos):
	"""
	To extract the sequence representing AMR gene from the path found by
	Bandage+BLAST presented in node_list; I could have used the original AMR gene
	sequence but I thought there might be cases that the assembler can't assemble
	the entire AMR gene or there are some errors in assembled one.
	Parameters:
		myGraph: The original graph
		node_list:	the list of nodes containing the AMR gene (i.e., path)
		orientation_list: list of orientation of nodes in the path
		start_pos:	the position of AMR in the first node from which the AMR gene has started
		end_pos: the position of AMR in the last node in which the AMR gene ended
	Return:
			the sequence of the AMR gene extracted from the path presented by node_list
	"""
	if not node_list:
		logging.error("ERROR: There is no node in node_list representing the AMR gene!")
		import pdb; pdb.set_trace()
		sys.exit()

	if len(node_list) == 1:
		return sequence_on_orientation(myGraph.segment(node_list[0]).sequence, orientation_list[0])[start_pos-1:end_pos]

	#Add first node
	found_amr_seq = sequence_on_orientation(myGraph.segment(node_list[0]).sequence, orientation_list[0])[start_pos-1:]
	#Add middle nodes
	if len(node_list) > 2:
		for i in range(len(node_list)-2):
			seq = sequence_on_orientation(myGraph.segment(node_list[i+1]).sequence, orientation_list[i+1])
			overlap_size = find_overlap(myGraph.segment(node_list[i]), myGraph.segment(node_list[i+1]),
										orientation_list[i], orientation_list[i+1])
			seq = seq[overlap_size:]
			found_amr_seq += seq
	#Add last node
	seq = sequence_on_orientation(myGraph.segment(node_list[-1]).sequence, orientation_list[-1])[:end_pos]
	overlap_size = find_overlap(myGraph.segment(node_list[-2]), myGraph.segment(node_list[-1]),
								orientation_list[-2], orientation_list[-1])
	seq = seq[overlap_size:]
	found_amr_seq += seq

	return found_amr_seq

def generate_sequence_path(myGraph, node_list, orientation_list, start_pos, end_pos,
							pre_sequence_list, post_sequence_list,
							pre_path_list, post_path_list, path_length_list,
							output_name, path_dir = 'same'):
	"""
	To concatenate  the sequences and paths before and after the AMR sequence.
	also, for any new sequence we add it if no similar enough sequence exists in the
	list. If such a sequence already exits in the list and its length is shorter,
	we replace it with the new sequence.
	e.g., pre_path_list = [['1-','2+']], post_path_list=[['7+'],['8+','9+','10-']],
	node_dir_list = ['[13+','14-]']
	- if path_dir = 'same' --> 		[
						['1-','2+','[13+','14-]','7+'],
						['1-','2+','[13+','14-]','8+','9+','10-']
									]
	- if path_dir = 'reverse' --> 	[
						['7-', '[14+', '13-]', '2-', '1+'],
						['10+', '9-', '8-', '[14+', '13-]', '2-', '1+']
									]
	Parameters:
		myGraph: The original graph
		node_list:	the list of nodes containing the AMR gene (i.e., path)
		orientation_list: list of orientation of nodes in the path
		start_pos:	the position of AMR in the first node from which the AMR gene has started
		end_pos: the position of AMR in the last node in which the AMR gene ended
		pre_sequence_list: the list of sequences preceding the AMR sequence in the graph
		post_sequence_list: the list of sequences following the AMR sequence in the graph
		pre_path_list: the list of nodes (and their orientation) preceding the AMR node
		post_path_list: the list of nodes (and their orientation) following the AMR node
		path_dir: 'same' if the AMR path direction (node_dir_list) is the same as what
			blast returned (presenting actual AMR sequence) and 'reverse' if the AMR path
			direction (node_dir_list) is the reverse of blast result (presenting the
			reverse complement of AMR sequence); in the latter, we need to return the
			reverse complement of the concatenated sequence to have the actual AMR
			sequence and not its reverse.

	"""
	#extract found AMR sequence
	found_amr_seq = extract_found_amr(myGraph, node_list, orientation_list, start_pos, end_pos)
	#create a temporaty directory
	temp_dir = 'temp_comparison2_'+output_name+'/'
	if not os.path.exists(temp_dir):
		try:
			os.makedirs(temp_dir)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
			pass
	#to be able to go over both 'for' loops make lists non-empty
	if not pre_path_list:
		pre_path_list = [[]]
	if not post_path_list:
		post_path_list = [[]]
	if not pre_sequence_list:
		pre_sequence_list = [['']]
	if not post_sequence_list:
		post_sequence_list = [['']]
	#add direction to nodes representing AMR gene
	node_orient_list = [node + orient for node, orient in zip(node_list, orientation_list)]
	#annotate the path representing AMR gene
	node_orient_list[0]='['+node_orient_list[0]
	node_orient_list[-1]=node_orient_list[-1]+']'
	#Generating all found sequences	and paths
	path_list = []
	sequence_list = []
	counter = 0
	path_info_list = []
	for pre_seq, pre_path in zip(pre_sequence_list, pre_path_list):
		for post_seq, post_path in zip(post_sequence_list, post_path_list):
			if path_dir == 'same':
				sequence = pre_seq.upper()+ found_amr_seq.lower() +post_seq.upper()
				path = pre_path +node_orient_list + post_path
			elif path_dir == 'reverse':
				sequence = rc(pre_seq.upper()+ found_amr_seq.lower() +post_seq.upper())
				path = reverse_path(pre_path +node_orient_list + post_path)
			index, found = similar_sequence_exits(sequence_list, sequence, temp_dir)
			if not found:
				sequence_list.append(sequence)
				path_list.append(path)
				path_info_list.append(path_length_list[counter])
			elif index>=0:
				sequence_list[index] = sequence
				path_list[index] = path
				path_info_list[index] = path_length_list[counter]
			counter+=1

	# delete the temp folder
	if os.path.exists(temp_dir):
		try:
			shutil.rmtree(temp_dir)
		except OSError as e:
			logging.error("Error: %s - %s." % (e.filename, e.strerror))

	return sequence_list, path_list, path_info_list

def append_path_sequence(sequence, path, sequence_list, path_list, output_dir,
							path_length, path_length_list):
	"""
	"""
	index, found = similar_sequence_exits(sequence_list, sequence, output_dir)
	if not found:
		sequence_list.append(sequence)
		path_list.append(path)
		path_length_list.append(path_length)
	elif index>=0:
		sequence_list[index] = sequence
		path_list[index] = path
		path_length_list[index] = path_length
	return sequence_list, path_list, path_length_list

def find_longest_post_neighbor(node, node_orient, node_list, both_dir):
	"""
	"""
	longest_edge = None
	max_length = 0
	for edge in (node.dovetails_L + node.dovetails_R):
		if len(edge.to_segment.sequence)>max_length and\
				edge.from_segment.name == node.name and edge.to_segment.name != node.name and\
				edge.to_segment.name not in node_list and edge.from_orient == node_orient:
			longest_edge = edge
			max_length = len(edge.to_segment.sequence)
		elif both_dir and len(edge.from_segment.sequence)>max_length and\
				edge.to_segment.name == node.name and edge.from_segment.name != node.name and\
				edge.from_segment.name not in node_list and edge.to_orient == reverse_sign(node_orient):
			longest_edge = edge
			max_length = len(edge.from_segment.sequence)
	return longest_edge

def find_longest_pre_neighbor(node, node_orient, node_list, both_dir):
	"""
	"""
	longest_edge = None
	max_length = 0
	for edge in (node.dovetails_L + node.dovetails_R):
		if len(edge.from_segment.sequence)>max_length and\
				edge.to_segment.name == node.name and edge.from_segment.name != node.name and\
				edge.from_segment.name not in node_list and edge.to_orient == node_orient:
			longest_edge = edge
			max_length = len(edge.from_segment.sequence)
		elif both_dir and len(edge.to_segment.sequence)>max_length and\
				edge.from_segment.name == node.name and edge.to_segment.name != node.name and\
				edge.to_segment.name not in node_list and edge.from_orient == reverse_sign(node_orient):
			longest_edge = edge
			max_length = len(edge.to_segment.sequence)
	return longest_edge

def extract_post_sequence_recursively_both_dir(node, node_orient, current_seq, current_path,
												length, sequence_list, path_list, node_list,
												compare_dir,length_thr, path_thr,
												current_path_length, path_length_list):
	"""
	To extract recursively the sequences following the AMR gene sequence and their paths
	In this function, we do this:
	- Find node's immediate neighbors like B
	- if there is an edge node --> B and the orient of node in that is the same as node_orient,
		B is eligible to be considered in the post_path for AMR sequence.
	- if there is an edge B --> node and the orient of node in that is reverse of
		node_orient, B with thereverse orient is eligible to be considered in the
		post_path for AMR sequence.
	Parameters:
		node:		the staring node in next paths
		node_orient:the orientation of the node in the edge this function instance was called from
		current_seq:the seq found so far
		current_path: the path found so far
		length: the remained length of the sequences around the AMR gene to be extracted
		sequence_list: the list of sequences following the AMR gene sequence
		path_list:	the list of nodes (and their orientation) following the nodes presenting the AMR gene
		node_list:	the list of nodes presenting the AMR gene
		length_thr: the threshold used for recursive pre_seq and
			post_seq until this percentage of the required length remained
			after which we just extract from the longest neighbor.
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
	Return:
		modified sequence_list and path_list
	"""
	seq = ""
	found_any_edge = False
	if length > 0 and len(current_path)<path_thr:
		for edge in (node.dovetails_L + node.dovetails_R):
			#if remained length is shorter than the threshold
			if ONLY_LONGEST_EDGE and length<=length_thr:
				import pdb; pdb.set_trace()
				longest_edge = find_longest_post_neighbor(node, node_orient, node_list, True)
				if longest_edge:
					edge = longest_edge
			#the second part of condition ensures that we are finding only nodes that are not presenting the AMR gene itself
			#Logically that shouldn't be the case unless there is a loop in the network:
			# path A -> B -> C represents the AMR; however we have an edge C -> A
			#so when we are looking for the nodes following AMR , A is selected too!!!!!
			to_segment = None
			to_orient = ''
			if edge.from_segment.name == node.name and edge.to_segment.name != node.name and\
					edge.to_segment.name not in node_list and edge.from_orient == node_orient:
				to_segment = edge.to_segment
				to_orient = edge.to_orient
			elif edge.to_segment.name == node.name and edge.from_segment.name != node.name and\
					edge.from_segment.name not in node_list and edge.to_orient == reverse_sign(node_orient):
				to_segment = edge.from_segment
				to_orient = reverse_sign(edge.from_orient)
			if to_segment and to_orient!='':
				#taking care of loops in the path
				index = exist_in_path(current_path, to_segment.name+to_orient)
				if index == -1:
					found_any_edge = True
					new_seq = sequence_on_orientation(to_segment.sequence, to_orient)
					#Remove the overlap between nodes' sequences
					overlap_size = find_overlap(edge.from_segment, edge.to_segment, edge.from_orient, edge.to_orient)
					new_seq = new_seq[overlap_size:]
					seq = current_seq + new_seq
					path=list.copy(current_path)
					path.append(str(to_segment.name)+str(to_orient))
					path_length = list.copy(current_path_length)
					path_length.append(min(len(new_seq), length))
					if len(new_seq) >= length:
						sequence_list, path_list, path_length_list =\
									append_path_sequence(seq[:len(current_seq)+length],
									path, sequence_list, path_list, compare_dir,
									path_length, path_length_list)
					else:
						sequence_list, path_list, path_length_list =\
									extract_post_sequence_recursively_both_dir(
									to_segment, to_orient, seq, path, length - len(new_seq),
									sequence_list, path_list, node_list, compare_dir,
									length_thr, path_thr,
									path_length, path_length_list)
				# graph loops are specified in { }
				elif index > -1:
					current_path[index] = '{'+current_path[index]
					current_path[-1]+='}'
			if ONLY_LONGEST_EDGE and length<=length_thr:
				#we only traverse the longest edge (already did) and not all edges
				break
	if not found_any_edge:
		sequence_list, path_list, path_length_list = append_path_sequence(current_seq,
							current_path, sequence_list, path_list, compare_dir,
							current_path_length, path_length_list)
	return sequence_list, path_list, path_length_list

def extract_post_sequence_recursively(node, node_orient, current_seq, current_path,
										length, sequence_list, path_list, node_list,
										compare_dir, length_thr, path_thr,
										current_path_length, path_length_list):
	"""
	To extract recursively the sequences following the AMR gene sequence and their paths
	Parameters:
		node:		the staring node in next paths
		node_orient:the orientation of the node in the edge this function instance was called from
		current_seq:the seq found so far
		current_path: the path found so far
		length: the remained length of the sequences around the AMR gene to be extracted
		sequence_list: the list of sequences following the AMR gene sequence
		path_list:	the list of nodes (and their orientation) following the nodes presenting the AMR gene
		node_list:	the list of nodes presenting the AMR gene
		length_thr: the threshold used for recursive pre_seq and
			post_seq until this percentage of the required length remained
			after which we just extract from the longest neighbor.
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
	Return:
		modified sequence_list and path_list

	"""
	seq = ""
	found_any_edge = False
	if length > 0 and len(current_path)<path_thr:
		for edge in (node.dovetails_L + node.dovetails_R):
			#if remained length is shorter than the threshold
			if ONLY_LONGEST_EDGE and length<=length_thr:
				longest_edge = find_longest_post_neighbor(node, node_orient, node_list, False)
				if longest_edge:
					edge = longest_edge
			#the second part of condition ensures that we are finding only nodes that are not presenting the AMR gene itself
			#Logically that shouldn't be the case unless there is a loop in the network:
			# path A -> B -> C represents the AMR; however we have an edge C -> A
			#so when we are looking for the nodes following AMR , A is selected too!!!!!
			if edge.from_segment.name == node.name and edge.to_segment.name != node.name and\
					edge.to_segment.name not in node_list and edge.from_orient == node_orient:
				#taking care of loops in the path
				index = exist_in_path(current_path, edge.to_segment.name+edge.to_orient)
				if index == -1:
					found_any_edge = True
					new_seq = sequence_on_orientation(edge.to_segment.sequence, edge.to_orient)
					#Remove the overlap between nodes' sequences
					overlap_size = find_overlap(node, edge.to_segment, node_orient, edge.to_orient)
					new_seq = new_seq[overlap_size:]
					seq = current_seq + new_seq
					path=list.copy(current_path)
					path.append(str(edge.to_segment.name)+str(edge.to_orient))
					path_length = list.copy(current_path_length)
					path_length.append(min(len(new_seq), length))
					if len(new_seq) >= length:
						sequence_list, path_list, path_length_list =\
								append_path_sequence(seq[:len(current_seq)+length],
								path, sequence_list, path_list, compare_dir,
								path_length, path_length_list)
					else:
						sequence_list, path_list, path_length_list =\
								extract_post_sequence_recursively(
								edge.to_segment, edge.to_orient, seq, path,
								length - len(new_seq), sequence_list, path_list,
								node_list, compare_dir, length_thr, path_thr,
								path_length, path_length_list)
				# graph loops are specified in { }
				elif index > -1:
					current_path[index] = '{'+current_path[index]
					current_path[-1]+='}'
			if ONLY_LONGEST_EDGE and length<=length_thr:
				#we only traverse the longest edge (already did) and not all edges
				break
	if not found_any_edge:
		sequence_list, path_list, path_length_list = append_path_sequence(current_seq, current_path,
										sequence_list, path_list, compare_dir,
										current_path_length, path_length_list)
	return sequence_list, path_list, path_length_list

def extract_post_sequence(node, node_orient, node_list, length, end_pos, compare_dir,
							remained_len_thr, path_thr, both_dir = BOTH_DIR_RECURSIVE):
	"""
	The initial function to extract the post_sequence of AMR.
	it adds the sequence following the AMR sequence (if there is any) in the last
	node in AMR path and if more is required, calls a recursive function to go over neighbors.
	Parameters:
		node:		the staring node in next paths
		node_orient:the orientation of the node in AMR path
		node_list:	the list of nodes presenting the AMR gene
		length: 	the length of the sequences around the AMR gene to be extracted
		end_pos: 	the position of AMR in the last node in which the AMR gene ended
		remained_len_thr: the threshold used for recursive pre_seq and
			post_seq until this percentage of the required length remained
			after which we just extract from the longest neighbor.
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
		both_dir:	if True we check node's orientation as well as their direction to find
		 	valid nodes in post_path/post_sequence
	Return:
		the lists of sequences and paths following AMR
	"""
	post_sequence_list = []
	post_path_list = []
	path_length = []
	path_length_list = []
	post_sequence = ''
	postfix_length = length
	if end_pos > 0:
		#attach the end of the AMR node (not included in AMR seq) to post_sequence
		postfix_length -= (len(node.sequence) - end_pos)
		post_sequence = sequence_on_orientation(node.sequence, node_orient)[end_pos:]
	#Find the sequence after the AMR gene
	if postfix_length <= 0:
		post_sequence = post_sequence[:length]
		post_sequence_list.append(post_sequence)
		path_length.append(len(post_sequence))
		path_length_list.append(path_length)
	#check all edges started from last_segment
	else:
		if len(post_sequence)>0:
			path_length.append(len(post_sequence))
		if not both_dir:
			post_sequence_list, post_path_list, path_length_list =\
									extract_post_sequence_recursively(
									node = node, node_orient = node_orient,
									current_seq = post_sequence, current_path = [],
									length = postfix_length, sequence_list = [],
									path_list = [], node_list = node_list,
									comapre_dir = compare_dir,
									length_thr = remained_len_thr, path_thr = path_thr,
									current_path_length = path_length,
									path_length_list = path_length_list)
		else:
			post_sequence_list, post_path_list, path_length_list =\
									extract_post_sequence_recursively_both_dir(
									node = node, node_orient = node_orient,
									current_seq = post_sequence, current_path = [],
									length = postfix_length, sequence_list = [],
									path_list = [], node_list = node_list,
									compare_dir = compare_dir,
									length_thr = remained_len_thr, path_thr = path_thr,
									current_path_length = path_length,
									path_length_list = path_length_list)

	return post_sequence_list, post_path_list, path_length_list

def extract_pre_sequence_recursively_both_dir(node, node_orient, current_seq, current_path,
												length, sequence_list, path_list, node_list,
												compare_dir, length_thr, path_thr,
												current_path_length, path_length_list):
	"""
	To extract recursively the sequences preceding the AMR gene sequence and their paths
	In this function, we do this:
	- Find node's immediate neighbors like B
	- if there is an edge B --> node and the orient of node in that is the same as node_orient,
		B is eligible to be considered in the pre_path for AMR sequence.
	- if there is an edge node --> B and the orient of node in that is reverse of
		node_orient, B with the reverse orient is eligible to be considered in the
		pre_path for AMR sequence.
	Parameters:
		node:		the staring node in next paths
		node_orient:the orientation of the node in the edge this function instance was called from
		current_seq:the seq found so far
		current_path: the path found so far
		length: the remained length of the sequences around the AMR gene to be extracted
		sequence_list: the list of sequences preceding the AMR gene sequence
		path_list:	the list of nodes (and their orientation) preceding the nodes presenting the AMR gene
		node_list:	the list of nodes presenting the AMR gene
		length_thr: the threshold used for recursive pre_seq and
			post_seq until this percentage of the required length remained
			after which we just extract from the longest neighbor.
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
	Return:
		modified sequence_list and path_list
	"""
	seq = ""
	found_any_edge = False
	if length > 0 and len(current_path)<path_thr:
		for edge in (node.dovetails_R + node.dovetails_L):
			#if remained length is shorter than the threshold
			if ONLY_LONGEST_EDGE and length<=length_thr:
				longest_edge = find_longest_pre_neighbor(node, node_orient, node_list, True)
				if longest_edge:
					edge = longest_edge
			#the second part ofcondition ensures that we are finding only nodes that are not presenting the AMR gene itself
			#Logically that shouldn't be the case unless there is a loop in the network:
			# path A -> B -> C represents the AMR; however we have an edge C -> A
			#so when we are looking for the nodes preceding AMR , C is selected too!!!!!
			from_segment = None
			from_orient = ''
			if edge.to_segment.name == node.name and edge.from_segment.name != node.name and\
					edge.from_segment.name not in node_list and edge.to_orient == node_orient:
				from_segment = edge.from_segment
				from_orient = edge.from_orient
			elif edge.from_segment.name == node.name and edge.to_segment.name != node.name and\
					edge.to_segment.name not in node_list and edge.from_orient == reverse_sign(node_orient):
					from_segment = edge.to_segment
					from_orient = reverse_sign(edge.to_orient)
			if from_segment and from_orient!='':
				#taking care of loops in the path
				index = exist_in_path(current_path, from_segment.name+from_orient)
				if index == -1:
					found_any_edge = True
					new_seq = sequence_on_orientation(from_segment.sequence, from_orient)
					#Remove the overlap between nodes' sequences
					overlap_size = find_overlap(edge.from_segment, edge.to_segment, edge.from_orient, edge.to_orient)
					new_seq = new_seq[:len(new_seq)-overlap_size]
					seq =  new_seq + current_seq
					path=list.copy(current_path)
					path.insert(0, str(from_segment.name) + str(from_orient))
					path_length = list.copy(current_path_length)
					path_length.insert(0, min(len(new_seq), length))
					if len(new_seq) >= length:
						sequence_list, path_list, path_length_list =\
									append_path_sequence(seq[len(new_seq)-length:],
									path, sequence_list, path_list, compare_dir,
									path_length, path_length_list)
					else:
						sequence_list, path_list, path_length_list =\
									extract_pre_sequence_recursively_both_dir(
									from_segment, from_orient, seq, path,
									length - len(new_seq), sequence_list,
									path_list, node_list, compare_dir,
									length_thr, path_thr, path_length,
									path_length_list)
				# graph loops are specified in { }
				elif index>-1:
					current_path[index] = current_path[index] + '}'
					current_path[0]='{' + current_path[0]
			if ONLY_LONGEST_EDGE and length<=length_thr:
				#we only traverse the longest edge (already did) and not all edges
				break
	if not found_any_edge:
		sequence_list, path_list, path_length_list = append_path_sequence(current_seq,
										current_path,sequence_list, path_list, compare_dir,
										current_path_length, path_length_list)
	return sequence_list, path_list, path_length_list

def extract_pre_sequence_recursively(node, node_orient, current_seq, current_path,
										length, sequence_list, path_list, node_list,
										compare_dir, length_thr, path_thr,
										current_path_length, path_length_list):
	"""
	To extract recursively the sequences preceding the AMR gene sequence and their paths
	Parameters:
		node:		the staring node in next paths
		node_orient:the orientation of the node in the edge this function instance was called from
		current_seq:the seq found so far
		current_path: the path found so far
		length: the remained length of the sequences around the AMR gene to be extracted
		sequence_list: the list of sequences preceding the AMR gene sequence
		path_list:	the list od nodes (and their orientation) preceding the nodes presenting the AMR gene
		node_list:	the list of nodes presenting the AMR gene
		length_thr: the threshold used for recursive pre_seq and
			post_seq until this percentage of the required length remained
			after which we just extract from the longest neighbor.
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
	Return:
		modified sequence_list and path_list
	"""
	seq = ""
	found_any_edge = False
	if length > 0 and len(current_path)<path_thr:
		for edge in (node.dovetails_R + node.dovetails_L):
			#if remained length is shorter than the threshold
			if ONLY_LONGEST_EDGE and length<=length_thr:
				longest_edge = find_longest_pre_neighbor(node, node_orient, node_list, False)
				if longest_edge:
					edge = longest_edge
			#the second part ofcondition ensures that we are finding only nodes that are not presenting the AMR gene itself
			#Logically that shouldn't be the case unless there is a loop in the network:
			# path A -> B -> C represents the AMR; however we have an edge C -> A
			#so when we are looking for the nodes preceding AMR , C is selected too!!!!!
			if edge.to_segment.name == node.name and edge.from_segment.name != node.name and\
					edge.from_segment.name not in node_list and edge.to_orient == node_orient:
				#taking care of loops in the path
				index = exist_in_path(current_path, edge.from_segment.name+edge.from_orient)
				if index == -1:
					found_any_edge = True
					new_seq = sequence_on_orientation(edge.from_segment.sequence, edge.from_orient)
					#Remove the overlap between nodes' sequences
					overlap_size = find_overlap(edge.from_segment, node, edge.from_orient, node_orient)
					new_seq = new_seq[:len(new_seq)-overlap_size]
					seq =  new_seq + current_seq
					path=list.copy(current_path)
					path.insert(0, str(edge.from_segment.name) + str(edge.from_orient))
					path_length = list.copy(current_path_length)
					path_length.insert(0, min(len(new_seq), length))
					if len(new_seq) >= length:
						sequence_list, path_list, path_length_list =\
									append_path_sequence(seq[len(new_seq)-length:],
									path, sequence_list, path_list, compare_dir,
									path_length, path_length_list)
					else:
						sequence_list, path_list, path_length_list =\
						 			extract_pre_sequence_recursively(
									edge.from_segment, edge.from_orient, seq, path,
									length - len(new_seq), sequence_list, path_list,
									node_list, compare_dir, length_thr, path_thr,
									path_length, path_length_list)
				# graph loops are specified in { }
				elif index>-1:
					current_path[index] = current_path[index] + '}'
					current_path[0]='{' + current_path[0]
			if ONLY_LONGEST_EDGE and length<=length_thr:
				#we only traverse the longest edge (already did) and not all edges
				break
	if not found_any_edge:
		sequence_list, path_list, path_length_list = append_path_sequence(current_seq,
									current_path, sequence_list, path_list,
									compare_dir, current_path_length, path_length_list)
	return sequence_list, path_list, path_length_list

def extract_pre_sequence(node, node_orient, node_list, length, start_pos, compare_dir,
							remained_len_thr, path_thr, both_dir = BOTH_DIR_RECURSIVE):
	"""
	The initial function to extract the pre_sequence of AMR.
	it adds the sequence preceding the AMR sequence (if there is any) in the first
	node in AMR path and if more sequence is required, calls a recursive function to go over neighbors.
	Parameters:
		node:		the staring node in next paths
		node_orient:the orientation of the node in AMR path
		node_list:	the list of nodes presenting the AMR gene
		length: 	the length of the sequences around the AMR gene to be extracted
		end_pos: 	the position of AMR in the last node in which the AMR gene ended
		remained_len_thr: the threshold used for recursive pre_seq and
			post_seq until this percentage of the required length remained
			after which we just extract from the longest neighbor.
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
		both_dir:	if True we check node's orientation as well as their direction to find
		 	valid nodes in pre_path/pre_sequence
	Return:
		the lists of sequences and paths preceding AMR

	"""
	pre_sequence_list = []
	pre_path_list = []
	pre_sequence = ''
	path_length = []
	path_length_list = []
	prefix_length = length
	if start_pos > 0:
		#attach the beginning of the AMR node (not included in AMR seq) to pre_sequence
		prefix_length -= (start_pos-1)
		pre_sequence = sequence_on_orientation(node.sequence, node_orient)[:start_pos-1]
	#Find the sequence before the AMR gene
	if prefix_length <= 0:
		pre_sequence = pre_sequence[-length:]
		pre_sequence_list.append(pre_sequence)
		path_length.append(len(pre_sequence))
		path_length_list.append(path_length)
	#check all edges ended at first node
	else:
		if len(pre_sequence)>0:
			path_length.append(len(pre_sequence))
		if not both_dir:
			pre_sequence_list, pre_path_list, path_length_list =\
									extract_pre_sequence_recursively(
									node = node, node_orient = node_orient,
									current_seq = pre_sequence, current_path = [],
									length = prefix_length, sequence_list = [],
									path_list = [], node_list = node_list,
									compare_dir = compare_dir,
									length_thr = remained_len_thr,path_thr = path_thr,
									current_path_length = path_length,
									path_length_list = path_length_list)
		else:
			pre_sequence_list, pre_path_list, path_length_list =\
									extract_pre_sequence_recursively_both_dir(
									node = node, node_orient = node_orient,
									current_seq = pre_sequence, current_path = [],
									length = prefix_length, sequence_list = [],
									path_list = [], node_list = node_list,
									compare_dir = compare_dir,
									length_thr = remained_len_thr, path_thr = path_thr,
									current_path_length = path_length,
									path_length_list = path_length_list)

	return pre_sequence_list, pre_path_list, path_length_list

def find_reverse_blast_path(myGraph, node_list, orientation_list, start_pos, end_pos):
	"""
	To reverse the AMR path returned by blast and also adjust start_pos and end_pos
	e.g., [A+, B-, C-] --> [C+, B+, A-]
							new_node_list = [C, B, A]
							new_orientation_list = [+, +, -]
							new_start_pos = len(C) - end_pos + 1
							new_end_pos = len(A) -  start_pos +1
	Parameters:
		myGraph: The assembly graph
		node_list:	the list of nodes containing the AMR gene (i.e., path)
		orientation_list: list of orientation of nodes in the AMR path
		start_pos:	the position of AMR in the first node from which the AMR gene has started
		end_pos: the position of AMR in the last node in which the AMR gene ended
	Return:
	"""
	node_list_reverse = list.copy(node_list)
	orientation_list_reverse = list.copy(orientation_list)
	#single node in AMR path
	if len(node_list)==1:
		node = myGraph.segment(node_list[0])
		orientation_list_reverse[0] = reverse_sign(orientation_list[0])
		start_pos_reverse = len(node.sequence)-end_pos+1
		end_pos_reverse = len(node.sequence)-start_pos+1
	#multiple nodes in AMR path
	elif len(node_list)>1:
		node_list_reverse.reverse()
		orientation_list_reverse.reverse()
		for i in range(len(orientation_list_reverse)):
			orientation_list_reverse[i]=reverse_sign(orientation_list_reverse[i])
		node1 = myGraph.segment(node_list_reverse[0])
		node2 = myGraph.segment(node_list_reverse[-1])
		start_pos_reverse = len(node1.sequence)-end_pos+1
		end_pos_reverse = len(node2.sequence)-start_pos+1

	return node_list_reverse, orientation_list_reverse, start_pos_reverse, end_pos_reverse

def write_paths_info_to_file(paths_info_list, paths_info_file, seq_counter):
	"""
	"""
	counter = seq_counter
	with open(paths_info_file,'a') as fd:
		writer = csv.writer(fd)
		for i, path_info in enumerate(paths_info_list):
			for node_info in path_info:
				counter = i+seq_counter+1
				writer.writerow([counter, node_info['node'], node_info['coverage'],
									node_info['start'], node_info['end']])
	return counter

def calculate_coverage(segment, max_kmer_size, node, assembler):
	"""
	To calculate node coverage based on assembler type
	Parameters:
		segment/node: the node whose covearge is supposed to eb calculated
		max_kmer_size: the max_kmer_size used by assembler
	Return:
		coverage

	"""
	if assembler == Assembler_name.metaspades or assembler == Assembler_name.bcalm:
		coverage = segment.KC/(len(segment.sequence)-max_kmer_size)
	elif assembler == Assembler_name.megahit:
		coverage = float(node.split('cov_')[1].split('_')[0])
	elif assembler == Assembler_name.metacherchant or assembler == Assembler_name.spacegraphcats :
		coverage = -1
	else:
		logging.error("no way of calculating node coverage has been defined for this assembler!")
		import pdb; pdb.set_trace()
		sys.exit()
	return coverage

def generate_node_range_coverage(myGraph, node_list, orientation_list, start_pos,
								end_pos, pre_path_list, pre_path_length_list,
								post_path_list, post_path_length_list,
								max_kmer_size, assembler = Assembler_name.metaspades):
	"""
	To generate a list of all nodes representing a sequence their start and end
	in the sequence and their coverage
	Parameters:
		myGraph: the assembly graph
		node_list: the list of nodes reprsenting AMR
		orientation_list: the orientation of nodes representing AMR
		start_pos: the start position of sequence in the first node in node_list
		end_pos: the end position of sequence in the last node in node_list
		pre_path_list: the node details for nodes representing upstream
		pre_path_length_list: the node length list for nodes representing upstream
		post_path_list: the node details for nodes representing downstream
		post_path_length_list: the node length list for nodes representing downstream
		max_kmer_size: the maximum kmer-size used by assembler
		assembler: the assembler used to generate the graph
	Results:
		the list of nodes and their start and end in the sequence for every extracted sequence
	"""
	if not pre_path_list:
		pre_path_list = [[]]
	if not post_path_list:
		post_path_list = [[]]
	#find amr_path_length_info
	start = 0
	amr_path_length_info = []
	for i, node in enumerate(node_list):
		segment = myGraph.segment(node)
		coverage = calculate_coverage(segment, max_kmer_size, node, assembler)
		#the length of first node in amr
		if i == 0 and len(node_list)==1:
			length = end_pos - start_pos + 1
		elif i==0 and len(node_list)>1:
			length = len(segment.sequence) -  start_pos + 1
		#the length of intermediate nodes in amr
		elif i < (len(node_list) - 1):
			overlap_size = find_overlap(myGraph.segment(node_list[i-1]), segment,
										orientation_list[i-1], orientation_list[i])
			length = len(segment.sequence) - overlap_size
		#the length of last node in amr
		else:
			overlap_size = find_overlap(myGraph.segment(node_list[i-1]), segment,
										orientation_list[i-1], orientation_list[i])
			length = end_pos - overlap_size
		node_info = {'node': node, 'coverage': coverage, 'start': start, 'end': start+length-1}
		amr_path_length_info.append(node_info)
		start =  start+length

	#pre_path_length_info
	pre_paths_info =[]
	for path, path_length in zip(pre_path_list, pre_path_length_list):
		start = 0
		pre_path_info=[]
		assert (len(path)==len(path_length) or len(path)==len(path_length) - 1),"inconsistent length of arrays: path vs path_length"
		difference = len(path_length) - len(path)
		end_common = len(path_length) -  difference
		for node, length in zip(path, path_length[:end_common]):
			pure_node = find_node_name(node)
			segment = myGraph.segment(pure_node)
			coverage = calculate_coverage(segment, max_kmer_size, pure_node, assembler)
			node_info = {'node': pure_node, 'coverage': coverage, 'start': start, 'end': start+length-1}
			start = start+length
			pre_path_info.append(node_info)
		if len(path)==len(path_length) - 1:
			segment = myGraph.segment(node_list[0])
			coverage = calculate_coverage(segment, max_kmer_size, node_list[0], assembler)
			node_info_last = {'node': node_list[0], 'coverage': coverage, 'start': start, 'end': start+path_length[-1]-1}
			pre_path_info.append(node_info_last)
		pre_paths_info.append(pre_path_info)

	#attach amr info to pre_path
	for i in range(len(pre_paths_info)):
		if len(pre_paths_info[i])>0:
			lag = pre_paths_info[i][-1]['end']+1
		else:
			lag=0
		for amr_info in amr_path_length_info:
			tmp = amr_info.copy()
			tmp['start'] += lag
			tmp['end'] += lag
			pre_paths_info[i].append(tmp)

	#post_path_length_info
	post_paths_info =[]
	for path, path_length in zip(post_path_list, post_path_length_list):
		start = 0
		post_path_info=[]
		assert (len(path)==len(path_length) or len(path)==len(path_length) - 1),"inconsistent length of arrays: path vs path_length"
		start_index = len(path_length) - len(path)
		if len(path)==len(path_length) - 1:
			segment = myGraph.segment(node_list[-1])
			coverage = calculate_coverage(segment, max_kmer_size, node_list[-1], assembler)
			node_info = {'node': node_list[-1], 'coverage': coverage, 'start': start, 'end': start+path_length[0]-1}
			post_path_info.append(node_info)
			start = start + path_length[0]
		for node, length in zip(path, path_length[start_index:]):
			pure_node = find_node_name(node)
			segment = myGraph.segment(pure_node)
			coverage = calculate_coverage(segment, max_kmer_size, pure_node, assembler)
			node_info = {'node': pure_node, 'coverage': coverage, 'start': start, 'end': start+length-1}
			start = start+length
			post_path_info.append(node_info)
		post_paths_info.append(post_path_info)

	#generate the entire path info by adding post_path
	paths_info = []
	for pre_path in pre_paths_info:
		if len(pre_path)>0:
			lag = pre_path[-1]['end']+1
		else:
			lag=0
		for post_path in post_paths_info:
			path_info = list.copy(pre_path)
			for node_info in post_path:
				tmp = node_info.copy()
				tmp['start']+=lag
				tmp['end']+=lag
				path_info.append(tmp)
			paths_info.append(path_info)

	return paths_info

def extract_neighborhood_sequence(gfa_file, length, amr_path_info, remained_len_thr,
									path_thr,output_name, max_kmer_size, seq_info,
									assembler = Assembler_name.metaspades):
	"""
	To extract all linear sequences with length = length from the start and end of the AMR gene
	In some cases, we might need to extract only the upstream or downstream
	Parameters:
		myGraph: The assembly graph
		length: the length of all sequences around the AMR gene to be extracted
		amr_path_info: contains node_list (the list of nodes containing the AMR gene (i.e., path)),
			their orientation, start_pos (the position of AMR in the first node from which
			the AMR gene has started) and end_pos (the position of AMR in the last node
			in which the AMR gene ended)
		remained_len_thr: the threshold used for recursive pre_seq and
			post_seq until this percentage of the required length remained
			after which we just extract from the longest neighbor.
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
		output_name: used for naming files
		max_kmer_size: the maximum kmer size used by the assembler
		seq_info: a dictionary to store upstream (presequence), downstream
			(postsequence) and their length
		assembler: the assembler used to assemble the graph
	Results:
		the list of extracted sequences and paths (the nodes representing the sequence)
			and their info as well as modified seq_info
	"""
	try:
		myGraph = gfapy.Gfa.from_file(gfa_file)
	except Exception as e:
		logging.error('Not loading the graph successfully: '+e)
		if assembler == Assembler_name.metacherchant:
			return [],[],[],[]
		else:
			import pdb; pdb.set_trace()
	node_list = amr_path_info['nodes']
	orientation_list = amr_path_info['orientations']
	start_pos = amr_path_info['start_pos']
	end_pos = amr_path_info['end_pos']

	last_segment = myGraph.segment(node_list[-1])
	if start_pos == 0:
		start_pos = 1
	if end_pos == 0:
		end_pos = len(str(last_segment.sequence))

	logging.debug('last_segment = '+last_segment.name+' start_pos = '+str(start_pos)+' end_pos= '+str(end_pos))
	#create a temporaty directory
	compare_dir = 'temp_comparison_'+output_name+'/'
	if not os.path.exists(compare_dir):
		try:
			os.makedirs(compare_dir)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
			pass

	#Find the sequences and paths for the path provided by bandage+blast for AMR gene
	if not seq_info['pre_seq']:
		#Find the sequence before the AMR gene
		logging.debug('Running extract_pre_sequence '+output_name+' ...')
		pre_sequence_list, pre_path_list, pre_path_length_list =\
		 							extract_pre_sequence(myGraph.segment(node_list[0]),
									orientation_list[0], node_list, length, start_pos,
									compare_dir, remained_len_thr, path_thr)
		seq_info['pre_seq'] = pre_sequence_list
		seq_info['pre_path'] = pre_path_list
		seq_info['pre_len'] = pre_path_length_list
	else:
		#up_stream has already found for another path with the same start node and position
		pre_sequence_list = seq_info['pre_seq']
		pre_path_list = seq_info['pre_path']
		pre_path_length_list = seq_info['pre_len']

	if not seq_info['post_seq']:
		#Find the sequence after the AMR gene
		logging.debug('Running extract_post_sequence '+output_name+' ...')
		post_sequence_list, post_path_list, post_path_length_list =\
									extract_post_sequence(last_segment,
									orientation_list[-1], node_list, length, end_pos,
									compare_dir, remained_len_thr, path_thr)
		seq_info['post_seq'] = post_sequence_list
		seq_info['post_path'] = post_path_list
		seq_info['post_len'] = post_path_length_list
	else:
		#down_stream has already found for another path with the same end node and position
		post_sequence_list = seq_info['post_seq']
		post_path_list = seq_info['post_path']
		post_path_length_list = seq_info['post_len']

	#combine path_info from pre and post
	logging.debug('Running generate_node_range_coverage '+output_name+' ...')
	path_length_list = generate_node_range_coverage(myGraph, node_list, orientation_list, start_pos,
							end_pos, pre_path_list, pre_path_length_list,
							post_path_list, post_path_length_list, max_kmer_size, assembler)
	#Combine pre_ and post_ sequences and paths
	logging.debug('Running generate_sequence_path '+output_name+' ...')
	sequence_list, path_list, path_info_list = generate_sequence_path(myGraph,
										node_list, orientation_list, start_pos,
										end_pos, pre_sequence_list,
										post_sequence_list, pre_path_list,
										post_path_list, path_length_list,
										output_name, 'same')


	if not BOTH_DIR_RECURSIVE:
		#Find the sequences and paths for the reverse of the path provided by bandage+blast for AMR gene
		node_list_reverse, orientation_list_reverse, start_pos_reverse, end_pos_reverse =\
			find_reverse_blast_path(myGraph, node_list, orientation_list, start_pos, end_pos)
		#Find the sequence before the AMR gene
		pre_sequence_list, pre_path_list, pre_path_length_list =\
								extract_pre_sequence(myGraph.segment(node_list_reverse[0]),
								orientation_list_reverse[0], node_list_reverse, length, start_pos_reverse,
								compare_dir, remained_len_thr, path_thr)
		#Find the sequence after the AMR gene
		post_sequence_list, post_path_list, post_path_length_list =\
								extract_post_sequence(myGraph.segment(node_list_reverse[-1]),
								orientation_list_reverse[-1], node_list_reverse, length, end_pos_reverse,
								compare_dir, remained_len_thr, path_thr)
		#Combine pre_ and post_ sequences and paths
		sequence_list_reverse, path_list_reverse = generate_sequence_path(myGraph,node_list_reverse,
											orientation_list_reverse, start_pos_reverse,
											end_pos_reverse, pre_sequence_list,
											post_sequence_list, pre_path_list, post_path_list,
											output_name, 'reverse')

		sequence_list, path_list = remove_identical_sub_sequences(sequence_list+sequence_list_reverse,
																	path_list+path_list_reverse)
	# delete the temp folder
	if os.path.exists(compare_dir):
		try:
			shutil.rmtree(compare_dir)
		except OSError as e:
			logging.error("Error: %s - %s." % (e.filename, e.strerror))

	return sequence_list, path_list, path_info_list, seq_info

def find_amr_related_nodes(amr_file, gfa_file, output_dir, bandage_path = BANDAGE_PATH,
							threshold =  95, output_pre = '', align_file = ''):
	"""
	Run bandage+blast to find the sequence in amr_file (as the query) in the assembly
	graph (gfa_file), and extract the path(s) representing the AMR sequence (i.e.,
	AMR path) in the assembly graph.
	e.g., (121) A+, B-, C+ (143) --> paths_info =	[
										{nodes:['A', 'B', 'C'],
										orientations: ['+', '-', '+'],
										start_pos: 121,
										end_pos: 143}
													]
	Parameters:
		amr_file: the FASTA file containing the AMR sequence (our query)
		gfa_file: the GFA file containing the assembly graph (our DB)
		output_dir: the output directory to store files
		bandage_path: the address of bandage executation file
		threshold: threshold for identity and coverage
		output_pre: used for naming output file
	Return:
		A boolean value which is True if any path was found and
		A list of dictionaries each denoting an AMR path
	"""
	if align_file =='':
		#Run bandage+blast
		output_name=output_dir+output_pre+'_align_'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		if os.path.isfile(output_name+'.tsv'):
			os.remove(output_name+'.tsv')
		command = bandage_path +' querypaths '+gfa_file+' '+amr_file+' '+output_name + ' --pathnodes 50'
		os.system(command)
		align_file = output_name+".tsv"
	#Process the output tsv file
	found, paths_info = read_path_info_from_align_file(output_name+".tsv", threshold)

	return found, paths_info



def check_if_similar_ng_extractions_exist(amr_path_info, amr_paths_info):
	"""
	To check the new AMR path found by alignment with the ones already processed!
	If there is a similar AMR pathin amr_paths_info, we don't need to process
	amr_path_info!
	Parameters:
		amr_path_info: the new AMR path
		amr_paths_info: the list of AMR paths processed so far
	Results:
		a dictionary containing the index of an entry from amr_paths_info with similar
		start node-position or end node-position
	"""
	found_up_stream = False
	found_down_stream = False
	similar_path = {'up_stream':-1, 'down_stream':-1}
	new_first_node = amr_path_info['nodes'][0]+amr_path_info['orientations'][0]
	new_last_node = amr_path_info['nodes'][-1]+amr_path_info['orientations'][-1]
	new_start_pos = amr_path_info['start_pos']
	new_end_pos = amr_path_info['end_pos']
	for i, path_info in enumerate(amr_paths_info):
		start_pos = path_info['start_pos']
		end_pos = path_info['end_pos']
		# if len(amr_path_info['nodes'])!=len(path_info) or (start_pos!=new_start_pos and end_pos!=new_end_pos):
		# 	continue
		if start_pos!=new_start_pos and end_pos!=new_end_pos:
			continue
		first_node = path_info['nodes'][0]+path_info['orientations'][0]
		last_node = path_info['nodes'][-1]+path_info['orientations'][-1]
		if len(path_info)==1 and len(amr_path_info)==1 and new_first_node==first_node:
			logging.error('there shouldnt be two separate amr paths with the same single node!')
			import pdb; pdb.set_trace()
		if new_first_node==first_node and new_start_pos==start_pos and\
			new_last_node==last_node and new_end_pos==end_pos:
			return {'up_stream':i, 'down_stream':i}

	for i, path_info in enumerate(amr_paths_info):
		start_pos = path_info['start_pos']
		end_pos = path_info['end_pos']
		if start_pos!=new_start_pos and end_pos!=new_end_pos:
			continue
		first_node = path_info['nodes'][0]+path_info['orientations'][0]
		last_node = path_info['nodes'][-1]+path_info['orientations'][-1]
		if not found_up_stream and new_first_node==first_node and new_start_pos==start_pos:
			similar_path['up_stream']=i
			found_up_stream = True
		elif not found_down_stream and new_last_node==last_node and new_end_pos==end_pos:
			similar_path['down_stream']=i
			found_dwon_stream = True
		if found_up_stream and found_down_stream:
			return similar_path

	return similar_path

def order_path_nodes(path_nodes, amr_file, out_dir, threshold = 90):
	"""
	Given that we have a list of nodes that are supposed to represent a given AMR
	(i.e., AMR path), this method returns their right order to represent the AMR
	sequence.
	Curretly, this method is only used for Metacherchant
	Parameters:
		path_nodes: the list of nodes representing AMR
		amr_file: the file containing AMR sequence
		out_dir: the dir to store some temporary files
		threshold: used for identity and coverage in bandage+blast
	Returns:
		the lists of sorted nodes and their corresponding orientation
	"""
	path_nodes_info = []
	no_path_nodes = []
	for i, node in enumerate(path_nodes):
		node_info_list = []
		#write the sequence into a fasta file
		query_file = create_fasta_file(node.sequence, out_dir, comment = ">"+node.name+"\n", file_name = 'query')
		#run blast query for alignement
		blast_file_name = out_dir+'blast.csv'
		command = 'blastn -query '+query_file+' -subject '+amr_file+\
			' -task blastn -outfmt 10 -max_target_seqs 10 -evalue 0.5 -perc_identity '+\
			str(threshold)+' > '+ blast_file_name
		os.system(command)
		with open(blast_file_name, 'r') as file1:
			myfile = csv.reader(file1)
			for row in myfile:
				identity=int(float(row[2]))
				coverage = int(float(row[3])/len(node.sequence)*100)
				if identity>=threshold and coverage>=threshold:
					node_info = {'name':node.name, 'c_start':int(row[8]), 'c_end':int(row[9])}
					node_info_list.append(node_info)
		if not node_info_list:
			no_path_nodes.append(i)
			logging.error(node.name+' was not found in the sequence of '+amr_file)
		path_nodes_info.append(node_info_list)
	#order nodes
	start_list = []
	orientations = []
	for path_info in path_nodes_info:
		if len(path_info)>0:
			if path_info[0]['c_start'] < path_info[0]['c_end']:
				start_list.append(path_info[0]['c_start'])
				orientations.append('+')
			else:
				start_list.append(path_info[0]['c_end'])
				orientations.append('-')
		else:
			start_list.append(-1)
			orientations.append('/')
	# start_list =[e[0]['c_start'] if len(e)>0 else -1 for e in path_nodes_info ]
	sorted_indeces = sorted(range(len(start_list)), key=lambda k: start_list[k])
	sorted_path_nodes = []
	sorted_orientations = []
	for index in sorted_indeces:
		if index not in no_path_nodes:
			sorted_path_nodes.append(path_nodes[index])
			sorted_orientations.append(orientations[index])

	return sorted_path_nodes, sorted_orientations

def extract_amr_align_from_file(gfa_file):
	"""
	Retrieve the list of segments that represent AMR path
	This method is use for Metacherchant in which such nodes ends with '_start'
	Parameters:
	 	gfa_file: the assembly graph file
	Return:
		the list of graph segments representing the AMR path
	"""
	myGraph = gfapy.Gfa.from_file(gfa_file)
	path_nodes = []
	for segment in myGraph.segments:
		if segment.name.endswith('_start'):
			path_nodes.append(segment)
	return path_nodes

def combine_nodes_orientations_metacherchant(node_list, orientations):
	"""
	"""
	#add direction to nodes representing AMR gene
	node_orient_list = [node + orient +'?' for node, orient in zip(node_list, orientations)]
	#annotate the path representing AMR gene
	node_orient_list[0]='['+node_orient_list[0]
	node_orient_list[-1]=node_orient_list[-1]+']'
	return node_orient_list

def combine_pre_post_metacherchant(pre_sequence_list, pre_path_list, post_sequence_list,
									post_path_list, seq_file, amr_seq, node_orient_list,
									compare_dir):
	"""
	To merge pre-seq and post-seq extracted from Metacherchant results
	"""
	sequence_list = []
	path_list = []
	counter = 0
	for pre_seq, pre_path in zip(pre_sequence_list, pre_path_list):
		for post_seq, post_path in zip(post_sequence_list, post_path_list):
			sequence = pre_seq.upper()+ amr_seq[:-1].lower() +post_seq.upper()
			path = pre_path +node_orient_list + post_path
			index, found = similar_sequence_exits(sequence_list, sequence, compare_dir)
			if not found:
				sequence_list.append(sequence)
				path_list.append(path)
			elif index>=0:
				sequence_list[index] = sequence
				path_list[index] = path
			counter+=1
	write_sequences_to_file(sequence_list, path_list, seq_file)

def ng_seq_extraction_metacherchant(gfa_file, length, output_dir,path_thr,
									remained_len_thr, output_name,max_kmer_size,
									seq_file, assembler = Assembler_name.metacherchant,
									threshold = 90, amr_file = ''):
	"""
	The core function to extract the neighborhood of AMRs for metacherchant
	Parameters:
		gfa_file:	the GFA file containing the assembly graph
		length:		the length of all sequences around the AMR gene to be extracted
		output_dir: the output directory to store files
		path_thr: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
		remained_len_thr: the threshold used for recursive pre_seq and
			post_seq until we have this length extracted
		output_name: used for naming output file
		max_kmer_size: the maximum kmer sized used by the assembler
		seq_file: the output file to store the extracted sequence
		assembler: the assembler used to generate the assembly graph
		threshold: 	threshold for identity and coverage
		amr_file:	the FASTA file containing the AMR sequence
	Return:
		the name of file containing the list of extracted sequences/paths
	"""
	with open(output_dir+"metacherchant_no_path.txt", 'a') as no_path_file:
		no_path_file.write(amr_file+'\n')
	try:
		myGraph = gfapy.Gfa.from_file(gfa_file)
	except Exception as e:
		logging.error(e)
		return ''
	#find nodes ending at _start as the nodes that create amr_path
	path_nodes = extract_amr_align_from_file(gfa_file)
	#find the order of these nodes in the amr path
	ordered_path_nodes, orientations = order_path_nodes(path_nodes, amr_file,
									output_dir+'alignment_files/', threshold)
	node_list = [e.name for e in ordered_path_nodes]

	last_segment = ordered_path_nodes[-1]
	start_pos = 1
	end_pos = len(str(last_segment.sequence))

	logging.debug('last_segment = '+last_segment.name+' start_pos = '+str(start_pos)+' end_pos= '+str(end_pos))
	#create a temporaty directory
	compare_dir = 'temp_comparison_'+output_name+'/'
	if not os.path.exists(compare_dir):
		try:
			os.makedirs(compare_dir)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
			pass
	amr_seq = retrieve_AMR(amr_file)

	#Process with the orientation found based on the alignment and ordering
	node_orient_list = combine_nodes_orientations_metacherchant(node_list, orientations)
	#Find the sequences and paths for the path for AMR gene
	#Find the sequence before the AMR gene
	logging.debug('Running extract_pre_sequence '+output_name+' ...')
	pre_sequence_list, pre_path_list, pre_path_length_list =\
	 							extract_pre_sequence(ordered_path_nodes[0],
								orientations[0], node_list, length, start_pos,
								compare_dir, remained_len_thr, path_thr)
	#Find the sequence after the AMR gene
	logging.debug('Running extract_post_sequence '+output_name+' ...')
	post_sequence_list, post_path_list, post_path_length_list =\
								extract_post_sequence(last_segment,
								orientations[-1], node_list, length, end_pos,
								compare_dir, remained_len_thr, path_thr)
	combine_pre_post_metacherchant(pre_sequence_list, pre_path_list, post_sequence_list,
										post_path_list, seq_file, amr_seq, node_orient_list,
										compare_dir)

	#Process with the reverse of the orientation found based on the alignment and ordering
	orientations[0]=reverse_sign(orientations[0])
	if len(orientations)>1:
		orientations[-1]=reverse_sign(orientations[-1])
	#add direction to nodes representing AMR gene
	node_orient_list = combine_nodes_orientations_metacherchant(node_list, orientations)
	#Find the sequences and paths for the path for AMR gene
	#Find the sequence before the AMR gene
	logging.debug('Running extract_pre_sequence '+output_name+' ...')
	pre_sequence_list, pre_path_list, pre_path_length_list =\
	 							extract_pre_sequence(ordered_path_nodes[0],
								orientations[0], node_list, length, start_pos,
								compare_dir, remained_len_thr, path_thr)
	#Find the sequence after the AMR gene
	logging.debug('Running extract_post_sequence '+output_name+' ...')
	post_sequence_list, post_path_list, post_path_length_list =\
								extract_post_sequence(last_segment,
								orientations[-1], node_list, length, end_pos,
								compare_dir, remained_len_thr, path_thr)
	combine_pre_post_metacherchant(pre_sequence_list, pre_path_list, post_sequence_list,
									post_path_list, seq_file, amr_seq, node_orient_list,
									compare_dir)
	logging.info("NOTE: The list of neighborhood sequences (extracted from assembly graph)\
	 		has been stroed in " + seq_file)
	# delete the temp folder
	if os.path.exists(compare_dir):
		try:
			shutil.rmtree(compare_dir)
		except OSError as e:
			logging.error("Error: %s - %s." % (e.filename, e.strerror))

	return seq_file

def neighborhood_sequence_extraction(gfa_file, length, output_dir,
									bandage = BANDAGE_PATH, threshold = 95,
									seq_name_prefix = 'ng_sequences_',
									#output_name = 'ng_sequences',
									path_node_threshold = 10 ,
									path_seq_len_percent_threshod = 90,
									max_kmer_size = 55,
									assembler = Assembler_name.metaspades,
									amr_seq_align_info = ''):
	"""
	The core function to extract the sequences/paths preceding and following the AMR sequence
	in the assembly graph
	Parameters:
		gfa_file:	the GFA file containing the assembly graph
		length:		the length of all sequences around the AMR gene to be extracted
		output_dir: the output directory to store files
		bandage: 	the address of bandage executation file
		threshold: 	threshold for identity and coverage
		seq_name_prefix: used for naming output file
		path_node_threshold: the threshold used for recursive pre_path and post_path
			search as long as the length of the path is less that this threshold
		path_seq_len_percent_threshod: the threshold used for recursive pre_seq and
			post_seq until we have this percentage of the required length
			after which we just extract from the longest neighbor.
		max_kmer_size: the maximum kmer used by the assembler
		assembler: the assembler used to generate the assembly graph
		amr_seq_align_info: a tuple containing the name of file containing amr sequence
			and the amr alignment info
	Return:
		the name of file containing the list of extracted sequences/paths
	"""
	amr_file, amr_paths_info = amr_seq_align_info
	logging.debug('amr_file = '+amr_file)
	output_name = seq_name_prefix +os.path.splitext(os.path.basename(amr_file))[0]
	remained_len_thr = length - (length*path_seq_len_percent_threshod/100.0)
	seq_output_dir = output_dir+'sequences/'
	if not os.path.exists(seq_output_dir):
		try:
			os.makedirs(seq_output_dir)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
			pass
	seq_file = seq_output_dir+output_name+'_'+str(length)+'_'+\
	datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')+'.txt'

	if not amr_paths_info:
		if not os.path.exists(output_dir+'alignment_files/'):
			try:
				os.makedirs(output_dir+'alignment_files/')
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
				pass
		#remained_len_thr = length - (length*path_seq_len_percent_threshod/100.0)
		#find all AMR paths in the assembly graph
		found, amr_paths_info = find_amr_related_nodes(amr_file, gfa_file, output_dir+'alignment_files/',
												bandage, threshold, output_name, '')
		if not found:
			if assembler==Assembler_name.metacherchant:
				logging.error("no alignment was found for "+amr_file)
				return ng_seq_extraction_metacherchant(gfa_file, length, output_dir,
												path_node_threshold,remained_len_thr,
												output_name,max_kmer_size, seq_file,
												assembler, threshold, amr_file), ''
			else:
				logging.error("no alignment was found for "+amr_file)
				#import pdb; pdb.set_trace()
				return '', ''

	#csv file for path_info
	if not os.path.exists(output_dir+'paths_info/'):
		try:
			os.makedirs(output_dir+'paths_info/')
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
			pass
	paths_info_file = output_dir+'paths_info/'+output_name+'_'+str(length)+'_'+\
	datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')+'.csv'
	with open(paths_info_file,'a') as fd:
		writer = csv.writer(fd)
		writer.writerow(['sequence', 'node', 'coverage', 'start', 'end'])
	logging.debug("Calling extract_neighborhood_sequence for "+os.path.basename(amr_file)+" ...")
	#Extract the sequenc of AMR neighborhood
	seq_counter = 0
	sequence_lists = []
	path_lists = []
	path_info_lists = []
	checked_amr_paths_info = []
	seq_info_list = []
	for i, amr_path_info in enumerate(amr_paths_info):
		seq_info = {'pre_seq':None, 'pre_path':None, 'pre_len':None,
			'post_seq':None, 'post_path':None, 'post_len':None}
		similar_path = check_if_similar_ng_extractions_exist(amr_path_info, checked_amr_paths_info)
		#logging.info('amr_path_info: '+str(amr_path_info)+' checked_amr_paths_info: '+str(checked_amr_paths_info)+' similar_path'+str(similar_path))
		if similar_path['up_stream']>-1 and similar_path['up_stream']==similar_path['down_stream']:
			#no need to save any information for this path
			continue
		elif similar_path['up_stream']==-1 and similar_path['down_stream']==-1:
			sequence_list, path_list, path_info_list, seq_info =\
								extract_neighborhood_sequence(gfa_file, length,
								amr_path_info, remained_len_thr, path_node_threshold,
								output_name, max_kmer_size, seq_info, assembler)
		elif similar_path['up_stream']>-1 and similar_path['down_stream']>-1:
			#we have extracted both its upstream and downstream but in different paths
			u_id = similar_path['up_stream']
			d_id = similar_path['down_stream']
			seq_info = {'pre_seq':seq_info_list[u_id]['pre_seq'],
						'pre_path':seq_info_list[u_id]['pre_path'],
						'pre_len':seq_info_list[u_id]['pre_len'],
						'post_seq':seq_info_list[d_id]['post_seq'],
						'post_path':seq_info_list[d_id]['post_path'],
						'post_len':seq_info_list[d_id]['post_len']}
			sequence_list, path_list, path_info_list, seq_info =\
								extract_neighborhood_sequence(gfa_file, length,
								amr_path_info, remained_len_thr, path_node_threshold,
								output_name, max_kmer_size, seq_info, assembler)
		elif similar_path['up_stream']>-1:
			#we need to extract its downstream
			u_id = similar_path['up_stream']
			seq_info['pre_seq'] = seq_info_list[u_id]['pre_seq']
			seq_info['pre_path'] = seq_info_list[u_id]['pre_path']
			seq_info['pre_len'] = seq_info_list[u_id]['pre_len']
			sequence_list, path_list, path_info_list, seq_info =\
								extract_neighborhood_sequence(gfa_file, length,
								amr_path_info, remained_len_thr, path_node_threshold,
								output_name, max_kmer_size, seq_info, assembler)

		elif similar_path['down_stream']>-1:
			#we need to extract its upstream
			d_id = similar_path['down_stream']
			seq_info['post_seq'] = seq_info_list[d_id]['post_seq']
			seq_info['post_path'] = seq_info_list[d_id]['post_path']
			seq_info['post_len'] = seq_info_list[d_id]['post_len']
			sequence_list, path_list, path_info_list, seq_info =\
								extract_neighborhood_sequence(gfa_file, length,
								amr_path_info, remained_len_thr, path_node_threshold,
								output_name, max_kmer_size, seq_info, assembler)
		if not sequence_list:
			continue
		seq_info_list.append(seq_info)
		sequence_lists.append(sequence_list)
		path_lists.append(path_list)
		path_info_lists.append(path_info_list)
		checked_amr_paths_info.append(amr_path_info)
		# if not sequence_list:
		# 	continue
		write_sequences_to_file(sequence_list, path_list, seq_file)
		logging.info("NOTE: The list of neighborhood sequences (extracted from assembly graph)\
	 		has been stroed in " + seq_file)
		seq_counter = write_paths_info_to_file(path_info_list, paths_info_file, seq_counter)
	return seq_file, paths_info_file

def neighborhood_graph_extraction(gfa_file, distance, output_dir,
								bandage = BANDAGE_PATH, threshold = 95,
								seq_name_prefix = 'ng_subgraph',
								amr_seq_align_info = ''):
	"""
	"""
	amr_file, paths_info = amr_seq_align_info
	logging.debug('amr_file = '+amr_file+'\t align_file = '+align_file)
	output_name = seq_name_prefix +os.path.splitext(os.path.basename(amr_file))[0]
	if not paths_info:
		if not os.path.exists(output_dir+'alignment_files/'):
			try:
				os.makedirs(output_dir+'alignment_files/')
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
				pass
		_, paths_info = find_amr_related_nodes(amr_file, gfa_file, output_dir+'alignment_files/',
												bandage, threshold, output_name, '')

	#Find neighbourhood of found nodes AND create a new graph contating the target subgraph
	subgraph_file_list =[]
	for i, path_info in enumerate(paths_info):
		node_list = path_info['nodes']
		#Find the list of segments and edges
		myGraph, segment_list, edge_list =extract_subgraph(node_list, distance, gfa_file)
		#Generate a graph with the lists of segments and edges
		subGraph = create_graph(myGraph, segment_list, edge_list)
		#write the subgraph in a GFA file
		subgraph_file = output_dir+output_name+'_'+str(distance)+'_'+str(i+1)+'_'+\
			datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')+'.gfa'
		subGraph.to_file(subgraph_file)
		logging.info("NOTE: The extracted subgraph has been stored in " + subgraph_file)
		subgraph_file_list.append(subgraph_file)

	return subgraph_file_list

if __name__=="__main__":

	text = 'This code is used to find the context of a given AMR gene'
	parser = argparse.ArgumentParser(description=text)
	parser.add_argument('--amr','-A', type=str, default = '',
		help = 'the path of the file containing the AMR gene sequence')
	parser.add_argument('--gfa', '-G', type=str, default='',
		help = 'the GFA file containing the graph')
	parser.add_argument('--distance', '-D', type = int, default=1,
		help = 'the maximum distance of neighborhood nodes to be extracted from the AMR gene')
	parser.add_argument('--length', '-L', type = int, default=1000,
		help = 'the length of AMR gene\'s neighbourhood to be extracted')
	parser.add_argument('--output_dir','-O', type=str, default = OUT_DIR,
		help = 'the output directory to store the results')
	args = parser.parse_args()

	if not os.path.exists(args.output_dir):
		os.makedirs(args.output_dir)

	if not args.amr:
		logging.error('please enter the path for the AMR gene file')
		import pdb; pdb.set_trace()
		sys.exit()

	if not args.gfa:
		logging.error('please enter the path for the assembly file')
		import pdb; pdb.set_trace()
		sys.exit()

	neighborhood_graph_extraction(args.amr,args.gfa, args.distance, args.output_dir,
								amr_seq_align_info = (arg.amr,''))
	neighborhood_sequence_extraction(args.gfa, args.length, args.output_dir,
								amr_seq_align_info = (arg.amr,''))
