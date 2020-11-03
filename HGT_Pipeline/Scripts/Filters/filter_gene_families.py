import os
import sys
import itertools
from Bio import SeqIO


rtg_files_handle = '../../ReadyToGo_Files'
og_files_handle = '../../allOG5Files'
params_handle = 'filtering_params.csv'
gen_trans_spreadsheet = 'ReadyToGo_file_types.csv'
output_handle = 'output.csv'


def bad_script_call():

	print('BAD SCRIPT CALL')
	
	exit()


def read_args():

	params_lines = [[val for val in line.split(',')] for i, line in enumerate(open(params_handle, 'r')) if i != 0 and i != 6]

	select = params_lines[:5]; filter = params_lines[5:13]; 
	use_trans = 'yes'; use_gen = 'yes'
	#use_trans = params_lines[17][1]; #use_gen = params_lines[18][1]

	coverage_threshold = 0
	try:
		coverage_threshold = int(params_lines[15][1])
	except:
		coverage_threshold = 0
		
	return [coverage_threshold, select, filter, use_trans, use_gen]	
	
	
def generate_gen_trans_spreadsheet():
	genomic = []
	transcriptomic = []
	
	for rtg_file in os.listdir(rtg_files_handle):
		if('ds_store' not in rtg_file.lower()):
			if('genom' in rtg_file.lower() or 'wgs' in rtg_file.lower() or 'wga' in rtg_file.lower()):
				genomic.append(rtg_file[:10])
			else:
				transcriptomic.append(rtg_file[:10])
				
	with open(gen_trans_spreadsheet, 'w') as o:
		for taxon in genomic:
			o.write(taxon + ',' + 'Genomic' + '\n')
		for taxon in transcriptomic:
			o.write(taxon + ',' + 'Transcriptomic' + '\n')

	
def get_abundance_by_code_section(type, coverage, use_trans, use_gen):

	og_counts_per_spec = {}
	
	transcriptomic_taxa = {}
	for line in open(gen_trans_spreadsheet, 'r'):
		if('transcript' in line.lower()):
			transcriptomic_taxa.update({line[:10] : None})	
			
	for rtg_file in os.listdir(rtg_files_handle):
		use_rtg_file = True	
		if(use_trans.lower() == 'no' and use_gen.lower() == 'yes' or use_gen.lower() == 'y'):
			if(rtg_file[:10] in transcriptomic_taxa):
				use_rtg_file = False
		if(use_gen.lower() == 'no' and use_trans.lower() == 'yes' or use_trans.lower() == 'y'):
			if(rtg_file[:10] not in transcriptomic_taxa):
				use_rtg_file = False
		if(use_gen.lower() == 'no' and use_trans.lower() == 'no'):
			use_rtg_file = False
	
		if('Store' not in rtg_file and use_rtg_file == True):			
			#Getting the ten digit code and the species code - this nomenclature handling is flexible
			if(type == 'major'):
				tdg_code = rtg_file[:2].lower()
			elif(type == 'minor'):
				tdg_code = rtg_file[:5].lower()
			elif(type == 'species'):
				tdg_code = rtg_file[:10].lower()
			else:
				bad_script_call()
			
			#Gathering a list of each og present in the file, and then another list with duplicate gene families removed
			if(coverage > 0 and rtg_file[:10] in transcriptomic_taxa):
				covs_in_file = [int(record.id.split('_')[7][3:]) for record in list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta"))]
				all_ogs = [record.id[-10:] for r, record in enumerate(list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta"))) if covs_in_file[r] > coverage]
			elif(coverage == 0):
				all_ogs = [record.id[-10:] for record in list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta"))]
					
			ogs_in_file = list(dict.fromkeys(all_ogs))
			
			#For each gene family present in the cell (file)
			for og in ogs_in_file:
				
				#Updating the proper species, incrementing its count for the current gene family by one
				try:
					og_counts_per_spec[og][tdg_code] += 1
				except KeyError:
					try:
						og_counts_per_spec[og].update({tdg_code : 1})
					except KeyError:
						og_counts_per_spec.update({og : {tdg_code : 1}})
							
	#Processing OrthoMCL data
	if(use_gen.lower() == 'yes' or use_gen.lower() == 'y'):		
		for og_file in os.listdir(og_files_handle):
			if('ds_store' not in og_file):
				taxa_in_file = list(dict.fromkeys([record.id[:10] for record in list(SeqIO.parse(og_files_handle + '/' + og_file, "fasta"))]))
					
				for taxon in taxa_in_file:
					if(type == 'major'):
						tdg_code = taxon[:2].lower()
					elif(type == 'minor'):
						tdg_code = taxon[:5].lower()
					elif(type == 'species'):
						tdg_code = taxon[:10].lower()
					else:
						bad_script_call()
				
					#Updating the proper species, incrementing its count for the current gene family by one
					try:
						og_counts_per_spec[og_file][tdg_code] += 1
					except KeyError:
						try:
							og_counts_per_spec[og_file].update({tdg_code : 1})
						except KeyError:
							og_counts_per_spec.update({og_file : {tdg_code : 1}})
													
	return og_counts_per_spec
	
	
def get_abundance_by_major_clade(coverage, use_trans, use_gen):
	return get_abundance_by_code_section('major', coverage, use_trans, use_gen)
	
	
def get_abundance_by_minor_clade(coverage, use_trans, use_gen):
	return get_abundance_by_code_section('minor', coverage, use_trans, use_gen)
	

def get_abundance_by_species(coverage, use_trans, use_gen):
	return get_abundance_by_code_section('species', coverage, use_trans, use_gen)
	
	
def clade_counts():
	major_clade_counts = { 'am' : 0, 'ba' : 0, 'ee' : 0, 'ex' : 0, 'op' : 0, 'pl' : 0, 'sr' : 0, 'za' : 0 }
	minors_per_major_counts = { 'am' : 0, 'ba' : 0, 'ee' : 0, 'ex' : 0, 'op' : 0, 'pl' : 0, 'sr' : 0, 'za' : 0 }
	species_per_genus_counts = {}
	minor_clade_counts = {}
	
	already_seen = {}
	all_taxa = []
	
	for rtg_file in os.listdir(rtg_files_handle):
		if('ds_store' not in rtg_file.lower()):
			all_taxa.append(rtg_file[:10])

	for og_file in os.listdir(og_files_handle):
		if('Store' not in og_file):
			all_taxa.extend(list(dict.fromkeys([record.id[:10] for record in list(SeqIO.parse(og_files_handle + '/' + og_file, "fasta"))])))
			
	all_taxa = list(dict.fromkeys(all_taxa))
		
	for taxon in all_taxa:
		try:
			minor_clade_counts[taxon[:5].lower()] += 1
		except KeyError:
			minor_clade_counts.update({taxon[:5].lower() : 1})
				
		major_clade_counts[taxon[:2].lower()] = major_clade_counts[taxon[:2].lower()] + 1
		
		if(taxon[:5] not in already_seen):
			minors_per_major_counts[taxon[:2].lower()] += 1
			already_seen.update({ taxon[:5].lower() : None })		
			
		
	return [major_clade_counts, minor_clade_counts, minors_per_major_counts, species_per_genus_count]
	
	
def filter(params):
	coverage, select_rows, filter_rows, use_trans, use_gen = params
			
	minor_clade_gfs = {}; species_gfs = {}
	major_clade_gfs = get_abundance_by_major_clade(coverage, use_trans, use_gen)
	if(select_rows[2][1] != '' or filter_rows[2][1] != '' or filter_rows[5][1] != ''):
		minor_clade_gfs = get_abundance_by_minor_clade(coverage, use_trans, use_gen)
	species_gfs = get_abundance_by_species(coverage, use_trans, use_gen)
	
	major_counts, minor_counts, minors_per_major_counts = clade_counts()
		
	gene_families_to_keep = []	
		
	#For every gene_family
	for gf in major_clade_gfs:
	
		keep_gf = True
		
		#Testing for major clades to keep
		for i, major_clade in enumerate(select_rows[0][1:]):
			if(major_clade != '' and '\n' not in major_clade): 
			
				thresh = select_rows[1][i+1]
				if(thresh == ''):
					thresh = select_rows[1][1]
				if(thresh == ''):
					bad_script_call()
																	
				if(major_clade.lower() in major_clade_gfs[gf]):
					flag = 0
					for species in species_gfs[og]:
						if(species not in transcriptomic_taxa):
							flag = 1
							break
						elif(species in transcriptomic_taxa):	
							for sub_species in species_gfs[og]:
								if(sub_species[:7] != species[:7] and sub_species in transcriptomic_taxa):
									flag = 1
									break
							if(flag == 1):
								break
					
					if(flag == 0):
						keep_gf = False
						break
				
					if( float(major_clade_gfs[gf][major_clade.lower()]) <= float(major_counts[major_clade.lower()]) * float(thresh) ):
						keep_gf = False
						break
				else:
					keep_gf = False
					break
				
		#Testing for minor clades to keep
		if(keep_gf == True):
			for i, minor_clade in enumerate(select_rows[2][1:]):
				if(minor_clade != '' and '\n' not in minor_clade): 
			
					thresh = select_rows[3][i+1]
					if(thresh == ''):
						thresh = select_rows[3][1]
					if(thresh == ''):
						bad_script_call()
																	
					if(minor_clade.lower() in minor_clade_gfs[gf]):
						if(float(minor_clade_gfs[gf][minor_clade.lower()]) <= float(minor_counts[minor_clade.lower()]) * float(thresh)):
							keep_gf = False
							break
					else:
						keep_gf = False
						break
		
		#Testing for species to keep
		if(keep_gf == True):
			for i, species in enumerate(select_rows[4][1:]):
				if(species != '' and '\n' not in species):
									
					if(species.lower() in species_gfs[gf]):
						if( float(species_gfs[gf][species.lower()]) == 0 ):
							keep_gf = False
							break
					else:
						keep_gf = False
						break					
		
		#Testing for major clades to filter out
		if(keep_gf == True):
			for i, major_clade in enumerate(filter_rows[0][1:]):
				if(major_clade != '' and '\n' not in major_clade): 
			
					thresh = filter_rows[1][i+1]
					if(thresh == ''):
						thresh = filter_rows[1][1]
					if(thresh == ''):
						bad_script_call()
				
					if(major_clade.lower() in major_clade_gfs[gf]):
						flag = 0
						for species in species_gfs[og]:
							if(species not in transcriptomic_taxa):
								flag = 1
								break
							elif(species in transcriptomic_taxa):	
								for sub_species in species_gfs[og]:
									if(sub_species[:7] != species[:7] and sub_species in transcriptomic_taxa):
										flag = 1
										break
								if(flag == 1):
									break
						
						if(flag == 0):
							break
				
						if( float(major_clade_gfs[gf][major_clade.lower()]) > float(major_counts[major_clade.lower()]) * float(thresh) ):
							keep_gf = False
							break
		
		#Testing for specific minor clades to filter out
		if(keep_gf == True):
			for i, minor_clade in enumerate(filter_rows[2][1:]):
				if(minor_clade != '' and '\n' not in minor_clade): 

					thresh = filter_rows[3][i+1]
					if(thresh == ''):
						thresh = filter_rows[3][1]
					if(thresh == ''):
						bad_script_call()
				
					if( float(minor_clade_gfs[gf][minor_clade.lower()]) > float(minor_counts[minor_clade.lower()]) * float(thresh) ):
						keep_gf = False
						break
						
		#Testing all other minor clades
		if(keep_gf == True):
			for i, major_clade in enumerate(filter_rows[5][1:]):
				if(major_clade != '' and '\n' not in major_clade): 
					
					inter_thresh = filter_rows[6][i+1]
					if(inter_thresh == ''):
						inter_thresh = filter_rows[6][1]
					if(inter_thresh == ''):
						bad_script_call()
												
					intra_thresh = filter_rows[7][i+1]
					if(intra_thresh == ''):
						intra_thresh = filter_rows[7][1]
					if(intra_thresh == ''):
						bad_script_call()
						
					minor_clades_counter = 0
					for minor_clade in minor_clade_gfs[gf]:
						use_mc = True
						if(major_clade in minor_clade):
							for mc_keep in select_rows[2][1:]:
								if(mc_keep in minor_clade):
									use_mc = False
									break
							for spec in select_rows[4][1:]:
								if(spec[3:5] in minor_clade):
									use_mc = False
									break
												
						if(use_mc == True and float(minor_clade_gfs[gf][minor_clade.lower()]) > float(minor_counts[minor_clade.lower()]) * float(intra_thresh)):
							minor_clades_counter += 1
												
					if(float(minor_clades_counter) > float(minors_per_major_counts[major_clade.lower()]) * float(inter_thresh)):
						keep_gf = False
						break						
		
		#Testing for species to filter out
		if(keep_gf == True):
			for i, species in enumerate(filter_rows[4][1:]):
				if(species != '' and '\n' not in species): 
					
					if( float(species_gfs[gf][species.lower()]) == 1 ):
						keep_gf = False
						break
	
		#Keep this gene family
		if(keep_gf == True):
			gene_families_to_keep.append(gf)
				
	return gene_families_to_keep
	
	
	
def main():
	generate_gen_trans_spreadsheet()

	gene_families_to_keep = filter(read_args())
	
	with open(output_handle, 'w') as o:
		for gf in gene_families_to_keep:
			o.write(gf + '\n')

main()
	