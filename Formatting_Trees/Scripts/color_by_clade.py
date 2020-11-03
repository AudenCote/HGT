import os 
import sys


dir_name = ''
file_names = []

minor_clades = []
colors = ['[&!color=#ff6288]', '[&!color=#ab2121]', '[&!color=#7b25aa]', '[&!color=#12aaff]', '[&!color=#006300]', '[&!color=#ffa100]', '[&!color=#000000]', '[&!color=#0000ff]']

taxon_colors = { 'ba' : '[&!color=#000000]', 'za' : '[&!color=#ff6288]', 'sr' : '[&!color=#7b25aa]', 'op' : '[&!color=#12aaff]', 'pl' : '[&!color=#006300]', 'ex' : '[&!color=#ffa100]', 'ee' : '[&!color=#ab2121]', 'am' : '[&!color=#0000ff]' }


def bad_script_call():
	print('\nInvalid inputs: please input the input file or directory and any minor clades you wish to color code:\n')
	print('If inputting one .tre file (do this relative to the location of this script):\n')
	print('python color_by_clade.py --input_file <input_file.tre> --minor_clades Ba_pb Ba_cy Za_em Sr_st\n\n')
	print('If inputting a directory of .tre files (do this relative to the location of this script):\n')
	print('python color_by_clade.py --input_dir <input_dir> --minor_clades Ba_pb Ba_cy Za_em Sr_st\n\n')
	print('You may choose to color code up to eight minor clades (see input format above). If you do not wish to input any minor clades to color code, omit this as an input and the script will default to color coding major clades automatically:\n')
	print('python color_by_clade.py --input_dir <input_dir or file>\n')
	
	exit()


def get_args():
	use_minor_clades = False
	directory = False
	default_trees_handle = ''
	try:
		if(sys.argv[1] == '--input_file'):
			default_trees_handle = sys.argv[2]
		elif(sys.argv[1] == '--input_dir'):
			directory = True
			default_trees_handle = sys.argv[2]
		try:
			if(sys.argv[3] == '--minor_clades'):
				use_minor_clades = True
				for i in range(4, 12):
					try:
						minor_clades.append(sys.argv[i])
					except:
						continue
		except:
			pass
					
	except:
		bad_script_call()
		
	return [default_trees_handle, use_minor_clades, directory]
	

def read_newick(input_handle, use_minor_clades, directory):

	mcandcol = {}
	if(use_minor_clades == True):
		try:
			for m, mc in enumerate(minor_clades):	
				mcandcol.update({mc.lower() : colors[m]})
		except IndexError:
			bad_script_call()

	newick = ''
	taxa_and_colors = []
	for line in open(input_handle, 'r'):
		temp = line.split(' ')[-1]
		if(temp[0] == '('):
			newick = temp
			line = line.split(',')
			for chunk in line:
				chunk = chunk.split('(')[-1].split(')')[0]
				if("'" in chunk):
					chunk = chunk.split("'")[1]
				
				try:
					#og_idx = chunk.index('OG5_')
					#taxon = chunk[0:og_idx + 10]
					taxon = chunk.split(':')[0]
				except:
					taxon = chunk[0:10]
				
				if(use_minor_clades == False):
					color = taxon_colors[taxon[:2].lower()]
					taxa_and_colors.append(taxon + color)
				else:
					try:
						color = mcandcol[taxon[:5].lower()]
						taxa_and_colors.append(taxon + color)
					except KeyError:
						taxa_and_colors.append(taxon)
					
	return [newick, taxa_and_colors]

def write_lines(o, newick, taxa_and_colors):
	ntax = str(len(taxa_and_colors))
			
	o.write('#NEXUS\n')	
	o.write('begin taxa;\n')
	o.write('\tdimensions ntax=' + ntax + ';\n')
	o.write('\ttaxlabels\n')
			
	for taxon in taxa_and_colors:
		o.write('\t' + taxon + '\n')
			
	o.write(';\nend;\n\n')
			
	o.write('begin trees;\n')
	o.write('\ttree tree_1 = [&R]\n')
	o.write(newick)
	o.write('end;\n\n')
			
	with open('figtree_format.txt', 'r') as ff:
		for line in ff:
			o.write(line)

def write_nexus(newick, taxa_and_colors, dir_name = '', directory = False, name_idx = 0):
	if(directory == False):
		with open(file_names[0][:-4] + '_colored.tre', 'w') as o:
			write_lines(o, newick, taxa_and_colors)
	else:
		try:
			os.mkdir(str(dir_name) + '_colored')
			with open(str(dir_name) + '_colored' + '/' + str(file_names[name_idx][:-4]) + '_colored.tre', 'w') as o:
				write_lines(o, newick, taxa_and_colors)
		except OSError:
			with open(str(dir_name) + '_colored/' + str(file_names[name_idx][:-4]) + '_colored.tre', 'w') as o:
				write_lines(o, newick, taxa_and_colors)
				

def main():
	dth, use_minor_clades, directory = get_args()
	if(directory == False):
		file_names.append(dth)
		newick, taxa_and_colors = read_newick(dth, use_minor_clades, directory)
		write_nexus(newick, taxa_and_colors)
	else:
		for f, file in enumerate(os.listdir(dth)):
			fname = dth + '/' + file
			file_names.append(file)
			newick, taxa_and_colors = read_newick(fname, use_minor_clades, directory)
			write_nexus(newick, taxa_and_colors, dth, directory, f)
	
	
main()