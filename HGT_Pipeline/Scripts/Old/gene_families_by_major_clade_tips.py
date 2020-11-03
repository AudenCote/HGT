
#Dependencies
import os
import sys
#For processing .fasta files
from Bio import SeqIO

#Name of directory containing ReadyToGo files to be processed
rtg_files_handle = 'ReadyToGo_Files'
#Name of output spreadsheet
output_handle = "gene_families_by_major_clade.csv"

#A list to hold the names of the collected major clades
major_clades = []
#A list to eventually contain all of the rows of the spreadsheet to be written
master_correspondence_list = []
#Iterating over all of the ReadyToGo files
for rtg_file in os.listdir(rtg_files_handle):
	
	#Printing out the name of the ReadyToGo file currently being processed
	if('Store' not in rtg_file):
		print('Processing ' + rtg_file[:10] + '. . .')

	#Collecting all of the gene family numbers in the current ReadyToGo file
	ogs_in_file = [record.id[-10:] for record in list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta"))]
	#Iterating all of the entries (and gene families) present in the file
	for og in ogs_in_file:
		correspondence_index = 0
		#Iterating over all of the currently known gene families
		if(len(master_correspondence_list) > 0):
			hit = False
			for o, master_og_entry in enumerate(master_correspondence_list):
				if(og == master_og_entry[0]):
					#Assigning the index in the master correspondence list to be the index of the known gene family if located
					correspondence_index = o
					hit = True
			
			#If the current gene family is not located in the master list:
			if(hit == False):
				new_og_entry = [0 for mc in master_correspondence_list[0]]
				new_og_entry[0] = og;
				#Make a new entry in the list for that gene family
				master_correspondence_list.append(new_og_entry)
				#Set the index of the known gene family in the correspondence list to be the last appended entry to the list
				correspondence_index = -1
		else:
			#If the current gene family is not located in the master list:
			new_og_entry = [og, 0];
			#Make a new entry in the list for that gene family
			master_correspondence_list.append(new_og_entry)
			#Set the index of the known gene family in the correspondence list to be the last appended entry to the list
			correspondence_index = -1
		
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
				for o, master_og_entry in enumerate(master_correspondence_list):
					master_correspondence_list[o].append(0)
				
		else:
			major_clades.append(current_major_clade)
			clade_subindex = 0
	
		#Incrementing the proper cell in the spreadsheet
		master_correspondence_list[correspondence_index][clade_subindex + 1] += 1
		
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
			
	





