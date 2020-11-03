#Dependencies
import os
import sys


spreadsheet_to_filter = sys.argv[1]
output_handle = sys.argv[2]
if(sys.argv[3] == '--abundance_threshold'):
	abundance_threshold_one = sys.argv[4]
	abundance_threshold_two = sys.argv[5]
if(sys.argv[6] == '--concentration_thresholds'):
	concentration_threshold_one = sys.argv[7]
	concentration_threshold_two = sys.argv[8]
	concentration_abundance_threshold = sys.argv[9]
clades_inputted = []
if(sys.argv[10] == '--select_for'):
	for e in range(11, 19):
		try:
			clades_inputted.append(sys.argv[e])
		except:
			break
	

#Name of directory containing ReadyToGo files to be processed
rtg_files_handle = '../ReadyToGo_Files/'

def get_major_clade_instances():
	major_clade_instances = []
	for l, line in enumerate(open(spreadsheet_to_filter, 'r')):
		if(l == 0):
			cells = line.split(',')
			for cell in cells:
				if(cell != '' and cell != ',' and cell != '\n'):
					major_clade_instances.append([cell.lower(), 0])
	
	return major_clade_instances

def get_abundance(major_clade_instances):
	
	######## Gathering a list containing the total number of species in each major clade ###########
	
	major_clade_counts = major_clade_instances
	for f, rtg_file in enumerate(os.listdir(rtg_files_handle)):
		for c, clade in enumerate(major_clade_counts):
			if(rtg_file[:2].lower() == clade[0]):
				major_clade_counts[c][1] += 1

	######### Calculating percentage of total species in each cell ###########
	
	new_lines = []
	for l, line in enumerate(open(spreadsheet_to_filter, 'r')):
		if(l != 0):
			new_line = []
			cells = line.split(',')
			og = cells[0]
			cells.pop(0);cells.remove('\n');
			for c, cell in enumerate(cells):
				if(cell != '' and cell != '\n'): 
					new_line.append(float(cell) / float(major_clade_counts[c][1]))
			new_line.insert(0, og)
			new_lines.append(new_line)
	
	return new_lines
	
def make_concentrated_relative(major_clade_instances, abundances):

	indices_to_keep = []
	for clade in clades_inputted:
		for c, mc in enumerate(major_clade_instances):
			if(mc[0] == clade):	
				indices_to_keep.append(c)
				
	major_clades = [clade[0] for clade in major_clade_instances]
	major_clade_indices = []
	for l, line in enumerate(open('../Master_spreadsheets/maximum_concentration_in_major_clade.csv', 'r')):
		if(l == 0):
			cells = line.split(',')
			for c, cell in enumerate(cells):
				for clade in major_clades:
					if(cell == clade):
						major_clade_indices.append(c)
			break
				
	new_lines = []
	for a, abundance_line in enumerate(abundances):
		for c, concentration_line in enumerate(open('../Master_spreadsheets/maximum_concentration_in_major_clade.csv', 'r')):
			concentration_line = concentration_line.split(',')
			if(a != 0 and c!= 0):
				if(abundance_line[0] == concentration_line[0]):
					new_line = []
					
					og = abundance_line[0]; abundance_line.pop(0); concentration_line.pop(0); concentration_line.remove('\n');
					concentration_line_filtered = [concentration_line[index - 1] for index in major_clade_indices]
					
					for cell_index, cell in enumerate(abundance_line):
						new_line.append([float(cell), float(concentration_line_filtered[cell_index])])
						
					append_line = True
					for v, val in enumerate(new_line):
						if(v in indices_to_keep):
							if(val[0] < float(abundance_threshold_one) or (val[1] > float(concentration_threshold_one) and val[0] > float(concentration_abundance_threshold))):
								append_line = False
								break
						else:
							if(val[0] > float(abundance_threshold_two) or (val[1] < float(concentration_threshold_two) and val[0] > float(concentration_abundance_threshold))):
								append_line = False
								break
					
					if(append_line == True):
						new_line.insert(0, og)
						print(new_line)
						new_lines.append(new_line)
						break
			
	return new_lines
								
def main():

	major_clade_instances = get_major_clade_instances()
	abundances = get_abundance(major_clade_instances)
	new_lines = make_concentrated_relative(major_clade_instances, abundances)
		
	with open(output_handle, 'w') as output_file:
		output_file.write(',')
		for clade in major_clade_instances:
			output_file.write(clade[0] + ',')
		output_file.write('\n')
		for line in new_lines:
			for e, entry in enumerate(line):
				if(e == 0):
					output_file.write(entry + ',')
				else:
					output_file.write(str(round(entry[0], 3)) + ' | ' + str(round(entry[1], 3)) + ',')
			output_file.write('\n')
	
	
main()	

			