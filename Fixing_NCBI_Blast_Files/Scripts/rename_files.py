#Dependencies
import os
import sys
#For processing .fasta files
from Bio import SeqIO

original_files_handle = '../Originals'


for org in os.listdir(original_files_handle):
	
	true_name = org[14:24]


	if('Store' not in org):
		for file in os.listdir(original_files_handle + '/' + org):
			if('AA.fasta' in file and '.oneHit' not in file):
				
				with open(original_files_handle + '/' + org + '/' + file, 'r') as f:
					
					records = SeqIO.parse(f, "fasta")
					
					file = true_name.join(file.split('Ba_cy_Prsp'))
					
					with open('../NCBI/' + file, 'w') as o:
						for record in records:
							record.id = true_name.join(record.id.split('Ba_cy_Prsp'))
							record.description = true_name.join(record.id.split('Ba_cy_Prsp'))
							
						
							SeqIO.write(record, o, 'fasta')
			
			elif('.oneHit' in file):
						
				with open(original_files_handle + '/' + org + '/' + file, 'r') as f:
					lines = []
					for line in f:
						if('Ba_cy_Prsp' in line):
							line = true_name.join(line.split('Ba_cy_Prsp'))
							
						lines.append(line)
						
					file = true_name.join(file.split('Ba_cy_Prsp'))
							
					with open('../Blast/' + file, 'w') as o:
						for line in lines:
							o.write(line)		
			
			else:
				break			
	
		