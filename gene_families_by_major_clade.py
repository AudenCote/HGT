

import os
import sys

from Bio import SeqIO

rtg_files_handle = sys.argv[1]

output_handle = "gene_families_by_major_clade.csv"


major_clades = []
master_correspondence_list = []
for rtg_file in os.listdir(rtg_files_handle):
	#print(rtg_file)
	ogs_in_file = [record.id[-10:] for record in list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta"))]
	for og in ogs_in_file:
		mcl_index = 0
		for o, master_og_entry in enumerate(master_correspondence_list):
			if(og == master_og_entry[0]):
				mcl_index = 0
				break;
				
			new_og_entry = [0 for mc in master_correspondence_list[0]]
			new_og_entry[0] = og;
			
			master_correspondence_list.append(new_og_entry)
			
		
		master_correspondence_list[mcl_index][c] += 1
			
	





