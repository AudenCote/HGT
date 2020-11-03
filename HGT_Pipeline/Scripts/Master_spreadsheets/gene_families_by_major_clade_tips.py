#Dependencies
import os
import sys
import itertools
#For processing .fasta files
from Bio import SeqIO

#Name of directory containing ReadyToGo files to be processed
rtg_files_handle = '../ReadyToGo_Files'
#Name of output spreadsheet
output_handle = "../species_per_major_clade_by_gene_family.csv"

all_gene_families = dict.fromkeys(list(itertools.chain.from_iterable([record.id[-10:] for record in list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta")) if 'OG5_' in record.id[-10:]] for rtg_file in os.listdir(rtg_files_handle) if('Store' not in rtg_file))))

for gene_family in all_gene_families:
	all_gene_families[gene_family] = { 'am' : 0, 'ba' : 0, 'ee' : 0, 'ex' : 0, 'op' : 0, 'pl' : 0, 'sr' : 0, 'za' : 0 }
	
for rtg_file in os.listdir(rtg_files_handle):
	if('Store' not in rtg_file):
	
		print('Processing ' + str(rtg:file[:10]) + '...')
		
		clade_code = rtg_file[0:2]
	
		#Collecting all of the gene family numbers in the current ReadyToGo file
		ogs_in_file = [record.id[-10:] for record in list(SeqIO.parse(rtg_files_handle + '/' + rtg_file, "fasta"))]
		#Iterating all of the entries (and gene families) present in the file
		for og in ogs_in_file:
			try:
				all_gene_families[og][clade_code.lower()] += 1
			except KeyError:
				continue		

with open(output_handle, 'w') as o:
	for gene_family in all_gene_families:
		o.write(gene_family + ',')	
		for clade in all_gene_families[gene_family]:
			o.write(clade + ',')
		break
	o.write('\n')
			
	for gene_family in all_gene_families:
		o.write(gene_family + ',')	
		for clade in all_gene_families[gene_family]:
			o.write(all_gene_families[gene_family][clade] + ',')
	o.write('\n')