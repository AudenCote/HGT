

#Dependencies
import os
import sys
#For processing .fasta files
from Bio import SeqIO

#Name of directory containing ReadyToGo files to be processed
rtg_files_handle = '../Test_RTGs'
#Name of output spreadsheet
output_handle = "gene_families_by_major_clade_no_duplicates_filtered_by_coverage.csv"

#A list to hold the names of the collected major clades
major_clades = []
#A list to eventually contain all of the rows of the spreadsheet to be written
master_correspondence_dict = {}
#Iterating over all of the ReadyToGo files
for rtg_file in os.listdir(rtg_files_handle):
	
	#Printing out the name of the ReadyToGo file currently being processed
	if('Store' not in rtg_file):
		print('Processing ' + rtg_file[:10] + '. . .')

	#Collecting all of the gene family numbers in the current ReadyToGo file
	ogs_in_file = list(dict.fromkeys([record.id[-10:] record in enumerate(list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta")))
	
	#Iterating all of the entries (and gene families) present in the file
	for contig_index, og in enumerate(ogs_in_file):
		try:
			#If the current gene family is present in the master list:
			current_major_clade = rtg_file[:2]
			#Check whether the current major clade is not in the master major clade list, and if it is not then append it onto that list and record its index in the master list
			if(len(major_clades) > 0):
				hit = False
				for i, known_major_clade in enumerate(major_clades):
					if(known_major_clade == current_major_clade):
						clade_subindex = i
						hit = True
				if(hit == False):
					major_clades.append(current_major_clade)
					for key in master_correspondence_dict:
						master_correspondence_dict[key].append(0)
				
			else:
				major_clades.append(current_major_clade)
				clade_subindex = 0
	
			#Incrementing the proper cell in the spreadsheet
			master_correspondence_dict[og][clade_subindex] += 1
		except KeyError:
			major_clades.pop(-1)
		
			try:
				master_correspondence_dict.update({og : [0 for mc in master_correspondence_list[0]]})
			except:
				master_correspondence_dict.update({og : [0]})
				
			current_major_clade = rtg_file[:2]
			
			if(len(major_clades) > 0):
				hit = False
				for i, known_major_clade in enumerate(major_clades):
					if(known_major_clade == current_major_clade):
						clade_subindex = i
						hit = True
				if(hit == False):
					major_clades.append(current_major_clade)
					for key in master_correspondence_dict:
						master_correspondence_dict[key].append(0)
				
			else:
				major_clades.append(current_major_clade)
				clade_subindex = 0
	
			#Incrementing the proper cell in the spreadsheet
			master_correspondence_dict[og][clade_subindex] += 1
								
	print('')

#Writing the output spreadsheet using the data collected above
with open(output_handle, 'w') as output_file:
	output_file.write(',')
	for clade in major_clades:
		output_file.write(clade + ',')
	output_file.write('\n')
	for line in master_correspondence_list:
		for entry in line:
			output_file.write(str(entry) + ',')
		output_file.write('\n')
			
