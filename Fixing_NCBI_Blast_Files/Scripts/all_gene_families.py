

#Dependencies
import os
import sys
#For processing .fasta files
from Bio import SeqIO

#Name of directory containing ReadyToGo files to be processed
rtg_files_handle = '../ReadyToGo_NTD'
#Name of output spreadsheet
output_gf_content_handle = "../gene_families_present_in_all_cells.csv'

#Keys are OG numbers and values are number of occurrences of that gene family
all_gene_families = {}

#This is the important function, which outputs all of the gene families with which to run PhyloTOL
def process_gfs(spec_counts):

	#For each ReadyToGO file
	for rtg_file in os.listdir(rtg_files_handle):
		
		#Gathering a list of each og present in the file, and then another list with duplicate gene families removed
		all_ogs = [record.id[-10:] for record in list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta"))]
		
		for og in ogs_in_file:
			try:
				all_gene_families[og] += 1
			except KeyError:
				all_gene_families.update({og : 1})
				
	for gf in all_gene_families:
		if(all_gene_families[gf] < 24):
			all_gene_families.pop(gf)
	
	
def main():
	process_gfs(cell_counts())
	
	with open(output_gf_content_handle, 'w') as o:
		for og in all_gene_families:
			o.write(str(og) + ',' + str(all_gene_families[og]) + '\n')
	
	
main()
	
	
	
	
	
	
	
	
	
	
		
	
	
