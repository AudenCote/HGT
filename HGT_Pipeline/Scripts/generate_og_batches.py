import os
import sys

#input filtered spreadsheet and directory where text files (each with five ogs) will go
input_file = sys.argv[1]
output_dir = sys.argv[2]

gene_families = []

batches = []

with open(input_file, 'r') as spreadsheet:
	for line in spreadsheet:
		if(line.split(',')[0] != ''):
			gene_families.append(line.split(',')[0])
		
for g, gf in enumerate(gene_families):
	if(g % 5 == 0):
		batch = []
		try:
			for i in range(5):
				batch.append(gene_families[g + i])
		except:
			for i in range(len(gene_families) % 5):
				batch.append(gene_families[g + i])
		batches.append(batch)
								
				
for b, batch in enumerate(batches):
	with open(output_dir + 'batch_' + str(b + 1) + '.txt', 'w') as o:
		for og in batch:
			o.write(og + '\n')