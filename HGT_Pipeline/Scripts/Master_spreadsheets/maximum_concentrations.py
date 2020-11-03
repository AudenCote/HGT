
#Dependencies
import os
import sys
#For processing .fasta files
from Bio import SeqIO

#Name of directory containing ReadyToGo files to be processed
rtg_files_handle = '../ReadyToGo_Files/'
#Name of output spreadsheet
numbers_output_handle = "../Master_spreadsheets/maximum_concentration_in_major_clade.csv"
names_output_handle = "../Master_spreadsheets/maximum_concentration_organisms.csv"

#A list to hold the names of the collected major clades
major_clades = []
#A list to eventually contain all of the rows of the spreadsheet to be written
master_correspondence_list = []
names_correspondence_list = []
#Iterating over all of the ReadyToGo files
r = 0
for f, rtg_file in enumerate(os.listdir(rtg_files_handle)):
	
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
				new_og_entry = [[0 for e in range(len(master_correspondence_list[0][-1]))] for mc in master_correspondence_list[0]]
				new_names_entry = [['' for e in range(len(master_correspondence_list[0][-1]))] for mc in master_correspondence_list[0]]
				new_og_entry[0] = og; new_names_entry[0] = og;
				#Make a new entry in the list for that gene family
				master_correspondence_list.append(new_og_entry)
				names_correspondence_list.append(new_names_entry)
				#Set the index of the known gene family in the correspondence list to be the last appended entry to the list
				correspondence_index = -1
		else:
			#If the current gene family is not located in the master list:
			new_og_entry = [og, [0]];
			new_names_entry = [og, ['']]
			#Make a new entry in the list for that gene family
			master_correspondence_list.append(new_og_entry)
			names_correspondence_list.append(new_names_entry)
			#Set the index of the known gene family in the correspondence list to be the last appended entry to the list
			correspondence_index = -1
		
		#If the current gene family is present in the master list:
		current_major_clade = rtg_file[:2].lower()
		#Check whether the current major clade is not in the master major clade list, and if it is not then append it onto that list and record its index in the master list
		if(len(major_clades) > 0):
			hit = False
			for i, known_major_clade in enumerate(major_clades):
				if(known_major_clade == current_major_clade):
					clade_subindex = i
					hit = True
			if(hit == False):
				r = 1
				major_clades.append(current_major_clade)
				for o, master_og_entry in enumerate(master_correspondence_list):
					master_correspondence_list[o].append([0])
					names_correspondence_list[o].append([''])
				
		else:
			major_clades.append(current_major_clade)
			clade_subindex = 0
	
		#Incrementing the proper cell in the spreadsheet	
		master_correspondence_list[correspondence_index][clade_subindex + 1][r-1] += 1
		names_correspondence_list[correspondence_index][clade_subindex + 1][r-1] = rtg_file[:10]
	
	#Buffer zero for next file - there will be one extra at the end.
	for e in range(len(master_correspondence_list)):
		master_correspondence_list[e][clade_subindex + 1].append(0)
		names_correspondence_list[e][clade_subindex + 1].append('')
	
	r += 1

	print('')
	
print('Writing Spreadsheets. . .')
print('')
		
numbers_spreadsheet_rows = []
names_spreadsheet_rows = []
for g, gene_family in enumerate(master_correspondence_list):
	numbers_spreadsheet_rows.append([gene_family[0]]); names_spreadsheet_rows.append([gene_family[0]]);
	for c, clade_entry in enumerate(gene_family):
		if(c != 0):
			sum_total = 0
			for intra_clade_entry in clade_entry:
				sum_total += intra_clade_entry
			
			nanargmax = clade_entry.index(max(clade_entry))
			name = names_correspondence_list[g][c][nanargmax]
			
			if(sum_total != 0):
				max_conc = round(float(max(clade_entry)) / float(sum_total), 3)
			else:
				max_conc = 0
				
			numbers_spreadsheet_rows[g].append(max_conc)
			names_spreadsheet_rows[g].append(name)
			
with open(numbers_output_handle, 'w') as output_file:
	output_file.write(',')
	for clade in major_clades:
		output_file.write(clade + ',')
	output_file.write('\n')
	for line in numbers_spreadsheet_rows:
		for entry in line:
			output_file.write(str(entry) + ',')
		output_file.write('\n')
	
with open(names_output_handle, 'w') as output_file:
	output_file.write(',')
	for clade in major_clades:
		output_file.write(clade + ',')
	output_file.write('\n')
	for line in names_spreadsheet_rows:
		for entry in line:
			output_file.write(str(entry) + ',')
		output_file.write('\n')
	


			
	





