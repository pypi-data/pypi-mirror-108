"""
File:		utils.py
Aythor:		Somayeh Kafaie
Date:		March 2021
Purpose:	containing all utility functions used in other files
"""

import sys
import os
import errno
import copy
import argparse
import enum
import logging
import re
import datetime
import csv
from csv import DictReader
import pandas as pd
import collections
import shutil

AMR_FAMILY_INFO = 'aro_index.tsv'

def extract_name_from_file_name(file_name):
	"""
	"""
	return os.path.splitext(os.path.basename(file_name))[0]

def amr_name_from_comment(amr_comment):
	"""
	"""
	amr_name = amr_comment.split('[')[0].split('|')[-1].strip().replace(' ','_').replace("'",';').replace('/', ']')
	return amr_name
	#amr_name_processed = ''.join(e for e in amr_name_processed1 if e.isalpha() or e.isnumeric() or e=='_' or e=='-')

def amr_name_from_title(amr_title):
	"""
	"""
	return amr_title.strip().replace(' ','_').replace("'",';').replace('/', ']')

def restricted_amr_name_from_modified_name(amr_name):
	"""
	"""
	amr_name1 = amr_name.replace(";",'SS')
	amr_name1 = ''.join(e for e in amr_name1 if e.isalpha() or e.isnumeric() or e=='_' or e=='-')
	return amr_name1

def retreive_original_amr_name(amr_name):
	"""
	"""
	return amr_name.replace(';', "'").replace(']', '/')

def create_fasta_file(seq, output_dir, comment = "> sequence:\n", file_name = 'temp'):
	"""
	To create a fasta file for a sequence
	Parameters:
		seq: the sequence to be written into the file
		output_dir: the output directory address
		comment: the comment to be written into fasta file
		file_name: the name of the fasta file
	Return:
		the address of the fasta file
	"""
	myfile_name = output_dir+file_name+'.fasta'
	if os.path.isfile(myfile_name):
		os.remove(myfile_name)
	myfile = open(myfile_name, 'w')
	myfile.write(comment)
	if not comment.endswith('\n'):
		myfile.write('\n')
	myfile.write(seq)
	if not seq.endswith('\n'):
		myfile.write('\n')
	myfile.close()
	return  myfile_name


def initialize_logger(output_dir, file_name = 'logfile.log'):
	"""
	"""
	#logging_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'logs')
	logging_dir = os.path.join(output_dir,'logs')
	try:
		os.makedirs(logging_dir)
	except OSError:
		pass
	log_file_path = os.path.join(logging_dir, file_name)
	logging.basicConfig(level=logging.DEBUG)
	#logging.basicConfig()
	log_formatter = logging.Formatter(
		"%(asctime)s [%(levelname)-5.5s]	%(message)s"
	)
	root_logger = logging.getLogger()
	file_handler = logging.FileHandler(log_file_path)
	file_handler.setFormatter(log_formatter)
	root_logger.addHandler(file_handler)
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(log_formatter)
	root_logger.addHandler(console_handler)

def check_reads(v):
	if isinstance(v, str):
		return v
	elif isinstance(v, list):
		if len(v)!=2:
			return False
		for item in v:
			if not isinstance(v, str):
				return False
		return v
	else:
		return False

def str2bool(v):
	"""
	To convert a string to a boolean value
	Parameter:
		v: the input string
	Return:
		the converted boolean value
	"""
	if isinstance(v, bool):
		return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

def print_params(params):
	"""
	"""
	mylog = '\n'.join(param for param in params)
	logging.info(mylog)

def verify_file_existence(myfile, param_file, message):
	"""
	This code is used to check if the required file exits either through running
	previous steps of the pipeline or passed by user (or in the param list)
	Parameters:
		myfile:	the file was supposed to be generated via previous steps of the pipeline
		param_file:	the file set by the user
		message:	error message in case no instance of the required file exists
	Return:
		the valid instance of the parameter to work with
	"""
	if myfile!="":
		return myfile
	elif param_file !="":
		if isinstance(param_file, str) and os.path.isfile(param_file):
			return param_file
		elif isinstance(param_file, list):
			error = False
			for file in param_file:
				if not isinstance(file, str) or not os.path.isfile(file):
					error = True
			if not error:
				return True
	logging.error("ERROR: "+message)
	sys.exit()

def retrieve_AMR(file_path):
	"""
	To read the AMR gene from the text file.
	Parameters:
		file_path:	the address of the file containing the AMR gene
	Return:
		the sequence of the AMR gene in lower case
	"""
	amr_name = ''
	with open(file_path) as fp:
		for i, line in enumerate(fp):
			#skip comment line
			if line.startswith('>'):
				amr_name = amr_name_from_comment(line[:-1])
				continue
			return line, amr_name

def reverse_sign(sign):
	"""
	To reverse the sign (+/-)
	Parameetr:
		sign: either + or -
	Return:
		the reverse sign
	"""
	if sign=='-':
		return '+'
	elif sign=='+':
		return '-'
	else:
		logging.error("ERROR: ivalid sign!")
		sys.exit()

def find_node_orient(node):
	"""
	To remove specific characters and return the last character of what remains
	as the orient of the node
	"""
	return re.sub('[]}]', '', node)[-1]

def find_node_name(node):
	"""
	To remove specific characters and return the rest except the last character
	as the node name
	"""
	return re.sub('[]{}[]','', node)[:-1]

def find_node_name_orient(node):
	"""
	To remove specific characters and return the rest as the name+orient of the node
	"""
	return re.sub('[]{}[]','', node)

def exist_in_path(path, mynode):
	"""
	To check if a given node exists in the path
	Parameters:
		path:	a list of nodes
		mynde:	the node to check if it is in the path
	Return:
		True if mynode is in the path; False otherwise
	"""
	for i, node in enumerate(path):
		if find_node_name_orient(node)==mynode:
			return i
	return -1

def extract_files(gfiles, message):
	"""
	To extract file(s) address from an object
	# if gfiles is a list and the first item is a file address (it would be more
	# accurate to check this for all items) return gfiles
	# else if gfiles is a file address return [gfiles] as a list with one item
	# else if gfiles is a directory address return the list of files in it
	Parameters:
		gfiles:		a string or list of strings
		message:	an error message in case that no file was extracted successfully
	Return:
		the list of file(s) address
	"""
	if isinstance(gfiles, list):
		#check if these are files (not directories)
		if os.path.isfile(gfiles[0]):
			return gfiles
		else:
			logging.error(message)
			sys.exit()
		#elif os.path.isdir(gfiles[0])
	elif os.path.isfile(gfiles):
		return [gfiles]
	elif os.path.isdir(gfiles):
		myfiles = [os.path.join(gfiles, f) for f in os.listdir(gfiles) \
							if os.path.isfile(os.path.join(gfiles, f))]
		return myfiles
	elif message!='':
		logging.error(message)
		sys.exit()

def extract_amr_names_from_alignment_files(align_files):
	"""
	"""
	amr_names = [os.path.basename(e).split('_align')[0] for e in align_files]
	return amr_names

def read_ref_neighborhoods_from_file(ref_ng_file):
	"""
	"""
	ng_lists = []
	amr_list = []
	with open(ref_ng_file) as myref:
		for line in myref:
			if line.startswith('>'):
				items = line.split('::')
				amr_name = items[0]
				contig_name = items[1][:-1]
			else:
				ng_item ={'contig':contig_name, 'seq':line[:-1]}
				if amr_name not in amr_list:
					amr_list.append(amr_name)
					ng_lists.append([ng_item])
				else:
					amr_index = amr_list.index(amr_name)
					ng_lists[amr_index].append(ng_item)

	return zip(amr_lists, ng_lists)

def read_ref_annotations_from_db(amr_groups_db, amr_name):
	"""
	"""
	headers = ['seq_name', 'seq_value','seq_length', 'gene', 'prokka_gene_name',
				'length','start_pos', 'end_pos', 'RGI_prediction_type']
	amr_group = amr_groups_db.get_group(amr_name)
	loc_groups = amr_group.groupby('gene_location')
	location_groups_name = list(loc_groups.groups)
	#extract up_stream info
	ref_up_info_list = []
	if 'up_stream' in location_groups_name:
		up_loc_group = loc_groups.get_group('up_stream')
		up_info_list = up_loc_group.groupby(['seq_name'])[headers].apply(lambda g: g.values.tolist())
		for item in up_info_list:
			seq_info = []
			for info in item:
				gene_info = dict(zip(headers, info))
				seq_info.append(gene_info)
			ref_up_info_list.append(seq_info)
	#extract down_stream info
	ref_down_info_list = []
	if 'down_stream' in location_groups_name:
		down_loc_group = loc_groups.get_group('down_stream')
		down_info_list = down_loc_group.groupby(['seq_name'])[headers].apply(lambda g: g.values.tolist())
		for item in down_info_list:
			seq_info = []
			for info in item:
				gene_info = dict(zip(headers, info))
				seq_info.append(gene_info)
			ref_down_info_list.append(seq_info)
	#extract amr info
	ref_amr_info_list = []
	if 'target_amr' in location_groups_name:
		amr_group = loc_groups.get_group('target_amr')
		amr_info_list = amr_group.groupby(['seq_name'])[headers].apply(lambda g: g.values.tolist())
		for item in amr_info_list:
			seq_info = []
			if len(item)<1:
				logging.error("there should be one AMR info per seq!")
				import pdb; pdb.set_trace()
			elif len(item)==1:
				seq_info = dict(zip(headers, item[0]))
			else:
				for info in item:
					gene_info = dict(zip(headers, info))
					seq_info.append(gene_info)
			ref_amr_info_list.append(seq_info)

	return ref_up_info_list, ref_amr_info_list, ref_down_info_list


#>>> x[0]
#[['bla', 'bla', 267, 35, 301], ['tnpR', 'tnpR', 252, 567, 818]]
#>>> x[0][0]
#['bla', 'bla', 267, 35, 301]
#>>> x[1]
#[['tnpR', 'tnpR', 354, 465, 818]]
#>>> x[1][0]
#['tnpR', 'tnpR', 354, 465, 818]

	# ref_up_info_lists = []
	# ref_down_info_lists = []
	# ref_amr_info_lists = []
	# ref_up_info_list = []
	# ref_down_info_list= []
	# ref_amr_info_list = []
	# with open(annotation_file) as fd:
	# 	myreader = DictReader(myfile)
	# 	old_amr = ''
	# 	for row in myreader:
	# 		cur_amr = row['target_amr']
	# 		gene_info = {'seq_name':row['seq_name'], 'seq_value':row['seq_value'],
	# 			'seq_length':int(row['seq_length']), 'gene':row['gene'],
	# 			'length':int(row['length']), 'start_pos':int(row['start_pos']),
	# 			'end_pos':int(row['end_pos'])}
	# 		if row['gene_location']=='up_stream':


def run_RGI(input_file, output_dir, seq_description, include_loose = False, delete_rgi_files = False):
	"""
	To run RGI and annotate AMRs in the sequence
	# To ensure consistency between Prokka and RGI findings, we annotate found proteins
	# by Prokka (instead of annotationg DNA sequences from scratch)
	Parameters:
		input_file: the file contating proteins annotated by Prokka
		output_dir:  the path for the output directory
		seq_description: a small description of the sequence used for naming
		include_loose: Whether to include loose annotations
	Return:
		the list of extracted annotation information for the sequence
	"""
	rgi_dir = output_dir +"rgi_dir"
	if not os.path.exists(rgi_dir):
		try:
			os.makedirs(rgi_dir)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise
			pass

	output_file_name = rgi_dir +"/rgi_output_"+seq_description+"_"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
	#remove any potential * from the sequence
	delete_a_string_from_file('*', input_file)
	command = "rgi main --input_sequence " + input_file + " --output_file " +\
		output_file_name +" --input_type protein --clean --exclude_nudge"
	if include_loose:
		command+=" --include_loose"
	#rgi main --input_sequence  <seq_file_name> --output_file <output_file_name> --clean --include_loose --exclude_nudge --low_quality
	os.system(command)
	seq_info_list = []
	if os.path.isfile(output_file_name + '.txt'):
		with open(output_file_name + '.txt', newline = '') as rgi_file:
			rgi_reader = csv.reader(rgi_file, delimiter='\t')
			next(rgi_reader)
			for row in rgi_reader:
				seq_info = {'ORF_ID':row[0], 'gene':row[8].strip(),
				'prediction_type':row[5].strip(), 'best_identities':float(row[9]),
				'family':row[16].strip()}
				seq_info_list.append(seq_info)
	else:
		logging.error("ERROR: RGI didn't run successfully!")
		sys.exit()
	#delete temp files
	if delete_rgi_files and os.path.isfile(output_file_name + '.txt'):
		os.remove(output_file_name + '.txt')
	if delete_rgi_files and os.path.isfile(output_file_name + '.json'):
		os.remove(output_file_name + '.json')

	return seq_info_list

def annotate_sequence(seq, seq_description, output_dir, prokka_prefix, use_RGI = True,\
						RGI_include_loose = False, delete_prokka_dir = False):
	"""
	To run Prokka for a sequence and extract required information from its
		generated output files
	Parameters:
		seq:	the sequence to be annotated
		seq_description: a small description of the sequence used for naming
		output_dir:  the path for the output directory
		use_RGI:	RGI annotations incorporated for AMR annotation
		prokka_prefix: to run prokka via docker or conda or any other source properly
	Return:
		the list of extracted annotation information for the sequence
	"""
	#write the sequence into a temporary file
	seq_file_name = create_fasta_file(seq, '', file_name='temp_'+seq_description)

	prokka_dir = 'prokka_dir_'+seq_description+'_'+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
	prefix_name = 'mygenome_'+seq_description
	# if os.path.exists(prokka_dir):
	# 	try:
	# 		shutil.rmtree(prokka_dir)
	# 	except OSError as e:
	# 		logging.error("Error: %s - %s." % (e.filename, e.strerror))
	command = prokka_prefix + 'prokka --metagenome --outdir '+\
		prokka_dir+' --prefix '+ prefix_name+' --fast --notrna '+seq_file_name
	os.system(command)
	#move prokka directory to the right address
	shutil.move(prokka_dir, output_dir+prokka_dir)
	prokka_dir = output_dir + prokka_dir
	RGI_output_list = None
	if use_RGI:
		RGI_output_list = run_RGI(prokka_dir+'/'+prefix_name+'.faa', output_dir, seq_description,
								RGI_include_loose, delete_prokka_dir)

	#Go over Prokka's output files and extract required information
	seq_info = []
	with open(prokka_dir+'/'+prefix_name+'.tsv') as tsvfile:
		reader = csv.reader(tsvfile, delimiter='\t')
		#skip the header
		next(reader)
		for row in reader:
			mygene = row[3].strip()
			split_gene = mygene.split('_')
			if len(split_gene)==2 and split_gene[1].isnumeric():
				mygene = split_gene[0]
			gene_info = {'locus_tag':row[0].strip(), 'gene':mygene,'length':row[2].strip(),
						'product':row[6].strip(),'start_pos':None, 'end_pos':None,
						'prokka_gene_name':mygene, 'RGI_prediction_type':None,
						'coverage':None, 'family': None, 'seq_value': seq[:-1],
						'seq_name':None, 'target_amr': None}
			seq_info.append(gene_info)
	counter = 0
	with open(prokka_dir+'/'+prefix_name+'.tbl', 'r') as read_obj:
		for line in read_obj:
			if line[0].isdigit():
				cells = line.split('\t')
				seq_info[counter]['start_pos'] = int(cells[0])
				seq_info[counter]['end_pos'] = int(cells[1])
				counter+=1

	#incorporate RGI findings into Prokka's
	if RGI_output_list:
		for item in RGI_output_list:
			for gene_info in seq_info:
				if item['ORF_ID'].split(' ')[0]==gene_info['locus_tag']:
					gene_info['gene'] = item['gene']
					gene_info['RGI_prediction_type'] = item['prediction_type']
					gene_info['family'] = item['family']
					break

	#remove temporary files and folder
	if os.path.isfile(seq_file_name):
		os.remove(seq_file_name)
	if delete_prokka_dir:
		try:
			shutil.rmtree(prokka_dir)
		except OSError as e:
			logging.error("Error: %s - %s." % (e.filename, e.strerror))

	return seq_info

def split_up_down_seq(sequence):
	"""
	"""
	up_found = False
	down_found = False
	up_seq = ''
	down_seq = ''
	for ch in sequence:
		if ch.isupper() and not up_found:
			up_seq+=ch
		elif ch.islower():
			up_found = True
			continue
		elif ch.isupper() and not down_found:
			down_seq+=ch

	return up_seq, down_seq

def split_up_down_info(sequence, seq_info):
	"""
	"""
	amr_start = -1
	amr_end = -1
	index = 0
	up_info = []
	down_info = []
	while index < len(sequence):
		if sequence[index].islower() and amr_start==-1:
			amr_start = index
		elif sequence[index].isupper() and amr_start>-1:
			amr_end=index-1
			break
		index+=1
	#if there is no downstream
	if amr_end==-1 and sequence[-1].islower():
		amr_end = len(sequence)-1
	elif amr_end==-1 or amr_start==-1:
		logging.error("No AMR sequence (lower case string) was found in "+sequence)
		import pdb; pdb.set_trace()
	#import pdb;pdb.set_trace()
	#find the gene has the most overlap with the found range
	overlap_thr = 50
	found = False
	amr_info = []
	for gene_info in seq_info:
		start, end = min(gene_info['start_pos'], gene_info['end_pos']), max(gene_info['start_pos'], gene_info['end_pos'])
		if end<amr_start:
			up_info.append(gene_info)
		elif start> amr_end:
			down_info.append(gene_info)
		else:
			# added by 1 because in string indecesstarts from 0
			diff = max((amr_start+1-start), 0)+max((end - (amr_end+1)), 0)
			if ((1-(float(diff)/(end-start)))*100)>overlap_thr:
				found = True
				gene_info['target_amr'] = 'yes'
				amr_info = gene_info
			elif start<amr_start:
				up_info.append(gene_info)
			else:
				down_info.append(gene_info)

	return found, amr_info, up_info, down_info, seq_info

def compare_two_sequences(seq1, seq2, output_dir, threshold = 90, switch_allowed = True,
		return_file = False, blast_ext = ''):
	"""
	To compare one sequence (shorter sequence) against the other one (longer sequence) using blastn
	"""
	#make sure seq1 is the longer sequence
	if switch_allowed and len(seq1)<len(seq2):
		seq1, seq2 = seq2, seq1
	#write the query sequence into a fasta file
	query_file_name = output_dir+'query.fasta'
	with open(query_file_name, 'w') as query_file:
		query_file.write('> query \n')
		query_file.write(seq2)
	#write the query sequence into a fasta file
	subject_file_name = output_dir+'subject.fasta'
	with open(subject_file_name, 'w') as subject_file:
		subject_file.write('> subject \n')
		subject_file.write(seq1)
	#run blast query for alignement
	blast_file_name = output_dir+'blast'+blast_ext+'.csv'
	command = 'blastn -query '+query_file_name+' -subject '+subject_file_name+\
		' -task blastn-short -outfmt 10  > '+ blast_file_name
	os.system(command)

	if return_file:
		return blast_file_name

	with open(blast_file_name, 'r') as file1:
		myfile = csv.reader(file1)
		for row in myfile:
			identity=int(float(row[2]))
			coverage = int(float(row[3])/len(seq1)*100)
			if identity>=threshold and coverage>=threshold:
				return True

	return False

def unnamed_genes_are_siginificantly_similar(gene_info1, gene_info2, threshold = 90):
	"""
	"""
	if gene_info1['gene']!='' or gene_info2['gene']!='':
		return False
	start1, end1 = min(gene_info1['start_pos'], gene_info1['end_pos']), max(gene_info1['start_pos'], gene_info1['end_pos'])
	seq1 = gene_info1['seq_value'][start1-1:end1-1]
	start2, end2 = min(gene_info2['start_pos'], gene_info2['end_pos']), max(gene_info2['start_pos'], gene_info2['end_pos'])
	seq2 = gene_info2['seq_value'][start2-1:end2-1]
	return compare_two_sequences(seq1, seq2, '', threshold)

def seqs_annotation_are_identical(seq_info1, seq_info2, threshold = 90):
	"""
	"""
	if len(seq_info1)==len(seq_info2):
		identical_rows = 0
		for i, gene_info1 in enumerate(seq_info1):
			gene_info2 = seq_info2[i]
			if (gene_info1['gene']==gene_info2['gene'] and gene_info1['gene']!='') or\
				(gene_info1['gene']==gene_info2['gene'] and\
				unnamed_genes_are_siginificantly_similar(gene_info1, gene_info2, threshold) ):
				identical_rows+=1
		if identical_rows == len(seq_info1):
			return True
	return False

def similar_seq_annotation_already_exist(seq_info_list, all_seq_info_lists, threshold = 90):
	"""
	To check if annotations found for the new sequence have already exists in the
	list of annotations extracted from other sequences.
	Parameters:
		seq_info_list: list of annotations of the new sequence
		all_seq_info_lists: list of annotations of the other sequences annotated so far
	Return:
		True if seq_info_list is identical to another list in all_seq_info_lists in
		terms of 'gene', 'length','start_pos' and 'end_pos' for all thei items
	"""
	found = False
	for seq_list in all_seq_info_lists:
		if seqs_annotation_are_identical(seq_info_list, seq_list, threshold):
		# if len(seq_list)==len(seq_info_list):
		# 	similar_rows = 0
		# 	for i, seq_info in enumerate(seq_info_list):
		# 		if (seq_info['gene']==seq_list[i]['gene'] and seq_info['gene']!='') or\
		# 			(seq_info['gene']==seq_list[i]['gene'] and\
		# 			unnamed_genes_are_siginificantly_similar(seq_info, seq_list[i], threshold = 90)):
		# 			#(seq_info['gene']==seq_list[i]['gene'] and seq_info['length']==seq_list[i]['length']):
		# 		# if (seq_info['gene']==seq_list[i]['gene'] or\
		# 		# 	(seq_info['gene']=='' and (seq_list[i]['gene']=='UNKNOWN' or\
		# 		# 								seq_list[i]['gene']==''))):
		# 		# 	if seq_info['length']==seq_list[i]['length'] or\
		# 		#  	(seq_info['start_pos']==seq_list[i]['start_pos'] and\
		# 		# 	seq_info['end_pos']==seq_list[i]['end_pos']):
		# 			similar_rows+=1
		# 	if similar_rows == len(seq_list):
			found = True
			break

	return found

def extract_up_down_from_csv_file(seq_info):
	"""
	"""
	up_info = []
	down_info = []
	amr_info = []
	amr_found = False
	for gene_info in seq_info:
		if gene_info['target_amr']=='yes':
			amr_info = gene_info
			amr_found = True
		elif not amr_found:
			up_info.append(gene_info)
		else:
			down_info.append(gene_info)

	return amr_found, up_info, down_info, amr_info

def extract_info_from_overlap_file(overlap_file_name):
	"""
	"""
	heads = []
	member_lists = []
	unique_amr_list = []
	with open(overlap_file_name, 'r') as read_obj:
		for line in read_obj:
			if ':' in line:
				items = line[:-1].split(':')
				if len(items[1])>0:
					heads.append(items[0])
					members = items[1].split(', ')
					member_lists.append(members)
				else:
					unique_amr_list.append(items[0])
	return heads, member_lists, unique_amr_list

def read_info_from_overlap_ref_files(overlap_file_name, ref_amr_files):
	"""
	"""
	unique_amr_files = []
	not_found_amr_names = []
	heads, member_lists, unique_amr_list = extract_info_from_overlap_file(overlap_file_name)
	unique_restricted_amr_names = [restricted_amr_name_from_modified_name(e) for e in heads + unique_amr_list]
	all_found_amr_names = heads + unique_amr_list + [e for list in member_lists for e in list]
	restricted_amr_names = [restricted_amr_name_from_modified_name(e) for e in all_found_amr_names]
	for ref_file in ref_amr_files:
		ref_name = extract_name_from_file_name(ref_file)
		if not ref_name in restricted_amr_names:
			_, amr_name = retrieve_AMR(ref_file)
			not_found_amr_names.append(amr_name)
		elif ref_name in unique_restricted_amr_names:
			unique_amr_files.append(ref_file)

	return unique_amr_files, not_found_amr_names, len(all_found_amr_names)

def extract_unique_align_files(all_align_files, unique_amr_files):
	"""
	"""
	amr_align_files = []
	if all_align_files:
		for amr_file in unique_amr_files:
			found_it= False
			amr_name = extract_name_from_file_name(amr_file)
			for align_file in all_align_files:
				if os.path.basename(align_file).startswith(amr_name+'_align'):
					found_it=True
					amr_align_files.append(align_file)
					break
			if not found_it:
				logging.error("no alignment was found for "+ amr_file)
				import pdb; pdb.set_trace()
	return amr_align_files

def extract_nodes_in_path(path):
	"""
	Parameters:
		path:	a list of nodes with -/+ tail and comma separated : e.g., '(1363) 69-, 2193+ (1786)'
	Return:
		node_list:	list of node numbers -> e.g., [69, 2193]
		orientation_list: list of orientation of nodes -> e.g., [-, +]
		start_pos:	where in the first node the sequence has started -> e.g., 1363
		end_pos:	where in the last node the sequence ended  -> e.g., 1786
	"""
	start_pos = 0
	end_pos = 0
	if path.startswith('('):
		index = path.find(')')
		start_pos = int(path[1:index])
	if path.endswith(')'):
		index = path.rfind('(')
		end_pos = int(path[index+1:-1])
	#Remove text between ()
	path = (re.sub("\((.*?)\)", "", path)).strip()
	node_list = []
	orientation_list = []
	nodes = path.split(',')
	for node in nodes:
		if '-' in node:
			orientation_list.append('-')
		else:
			orientation_list.append('+')
		node = re.sub('[+-]', '', node.split()[0])
		node_list.append(node)
	return node_list, orientation_list, start_pos, end_pos

def read_path_info_from_align_file(align_file, threshold =  95):
	paths_info = []
	found = False
	with open(align_file) as tsvfile:
		reader = csv.reader(tsvfile, delimiter='\t')
		#skip the header
		next(reader)
		for row in reader:
			coverage = float(re.sub('[%]','',row[3]))
			identity = float(re.sub('[%]','',row[5]))
			if int(coverage) >= threshold and int(identity)>=threshold:
				found = True
				cell_info = row[1].strip()
				nodes, orientation_list, start_pos, end_pos = extract_nodes_in_path(cell_info)
				path_info = {'nodes':nodes, 'orientations':orientation_list,
								'start_pos':start_pos, 'end_pos':end_pos}
				paths_info.append(path_info)
	if not found:
		logging.info('ERROR: no path info was found in '+align_file)
	return found, paths_info

def read_path_info_from_align_file_with_multiple_amrs(align_file, threshold =  99):
	"""
	"""
	paths_info_list = collections.defaultdict(list)
	with open(align_file) as tsvfile:
		reader = csv.reader(tsvfile, delimiter='\t')
		#skip the header
		next(reader)
		for row in reader:
			amr_name = restricted_amr_name_from_modified_name(
				row[0].split('|')[-1].strip().replace(' ','_').replace("'",';'))
			coverage = float(re.sub('[%]','',row[3]))
			identity = float(re.sub('[%]','',row[5]))
			if int(coverage) >= threshold and int(identity)>=threshold:
				cell_info = row[1].strip()
				nodes, orientation_list, start_pos, end_pos = extract_nodes_in_path(cell_info)
				path_info = {'nodes':nodes, 'orientations':orientation_list,
								'start_pos':start_pos, 'end_pos':end_pos}
				paths_info_list[amr_name].append(path_info)
	return paths_info_list

def extract_path_info_for_amrs(all_align_files, unique_amr_files,amr_count, threshold):
	"""
	"""
	if len(all_align_files)==amr_count:
		amr_align_files = extract_unique_align_files(all_align_files, unique_amr_files)
		for align_file in amr_align_files:
			found, paths_info = read_path_info_from_align_file(align_file, threshold)
			if found:
				unique_amr_path_list.append(paths_info)
			else:
				logging.error(align_file + " file was not found or was empty!")
				import pdb; pdb.set_trace()
	else:
		paths_info_group_list = []
		for align_file in all_align_files:
			paths_info_group = read_path_info_from_align_file_with_multiple_amrs(
										align_file, threshold)
			paths_info_group_list.append(paths_info_group)
		unique_amr_path_list = []
		for amr_file in unique_amr_files:
			amr_found = False
			restricted_amr_name = extract_name_from_file_name(amr_file)
			for paths_info_group in paths_info_group_list:
				if restricted_amr_name in paths_info_group:
					amr_found = True
					path_info = paths_info_group[restricted_amr_name]
					unique_amr_path_list.append(path_info)
			if not amr_found:
				logging.error('ERROR: no path info was found for '+restricted_amr_name)
				import pdb; pdb.set_trace()
	return unique_amr_path_list


def concatenate_files(ref_files, final_file = 'metagenome.fasta'):
	"""
	To concatenate some files into a single file OR more specifically
	to create a metagenome sample from some genomes
	Parameters:
		ref_files:	the list of reference genomes in which AMR gene is supposed to be inserted
		final_file: the address of the metagenome file
	Return:
		The address of final_file
	"""
	for myfile in ref_files:
		command = 'cat '+myfile+' >> ' + final_file
		os.system(command)
	return final_file

def extract_family_of_amrs(info_file = '/media/Data/PostDoc/Dalhousie/Work/Test2/aro_index.tsv'):
	"""
	"""
	amr_family = collections.defaultdict(lambda: '')
	with open(info_file, 'r') as myfile:
		myreader = DictReader(myfile, delimiter='\t')
		for row in myreader:
			gene_name = row['Model Name'].strip()
			family_name =row['AMR Gene Family'].strip()
			amr_family[gene_name]=family_name
	return amr_family
def extract_amr_family_info(file_name = AMR_FAMILY_INFO):
	"""
	To extract the list of AMR families and their corresponding AMR genes from a
	CARD excel sheet
	"""
	family_list = []
	family_info = []
	with open(file_name, 'r') as myfile:
		myreader = DictReader(myfile, delimiter='\t')
		for row in myreader:
			gene_name = amr_name_from_title(row['Model Name'])
			if row['AMR Gene Family'] not in family_list:
				family_list.append(row['AMR Gene Family'])
				family_info.append([gene_name.lower()])
			else:
				myindex = family_list.index(row['AMR Gene Family'])
				family_info[myindex].append(gene_name.lower())

	return {'family':family_list, 'gene_list':family_info}

def delete_lines_started_with(ch, filename):
	"""
	To delete all the lines in a text file that starts with a given character
	Parameters:
		ch: the character
		filename: the text file
	"""
	# command = "sed -i '/^P/d' " + file_name
	# os.system(command)
	file1 = open(filename, 'r')
	file2 = open('temp.txt', 'w')
	for line in file1.readlines():
		if not (line.startswith(ch)):
			file2.write(line)
	file1.close()
	file2.close()
	os.rename('temp.txt', filename)

def delete_a_string_from_file(ch, filename):
	"""
	To delete a given character or string from a file
	Parameters:
		ch: the character or string to be deleted
		filename: the text file
	"""
	# command = "sed -i 's/*//g' " + input_file
	# os.system(command)
	with open(filename, 'r') as infile, open('temp.txt', 'w') as outfile:
		data = infile.read()
		data = data.replace(ch,'')
		outfile.write(data)
	os.rename('temp.txt', filename)
