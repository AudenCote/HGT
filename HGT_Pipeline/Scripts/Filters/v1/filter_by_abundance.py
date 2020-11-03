#Dependencies
import os
import sys


spreadsheet_to_filter = sys.argv[1]
output_handle = sys.argv[2]
if(sys.argv[3] == '--thresholds'):
	threshold_one = float(sys.argv[4])
	threshold_two = float(sys.argv[5])
clades_inputted = []
if(sys.argv[6] == '--select_for'):
	for e in range(7, 15):
		try:
			clades_inputted.append(sys.argv[e])
		except:
			break
	

#Name of directory containing ReadyToGo files to be processed
rtg_files_handle = '../../ReadyToGo_Files/'

def get_major_clade_instances():
	major_clade_instances = []
	for l, line in enumerate(open(spreadsheet_to_filter, 'r')):
		if(l == 0):
			cells = line.split(',')
			for cell in cells:
				if(cell != '' and cell != ',' and cell != '\n'):
					major_clade_instances.append([cell.lower(), 0])
	
	return major_clade_instances

def percent_total_species(major_clade_instances, threshold_one, threshold_two):

	indices_to_keep = []
	for clade in clades_inputted:
		for c, mc in enumerate(major_clade_instances):
			if(mc[0] == clade):	
				indices_to_keep.append(c)
	
	######## Gathering a list containing the total number of species in each major clade ###########
	
	major_clade_counts = major_clade_instances
	for f, rtg_file in enumerate(os.listdir(rtg_files_handle)):
		for c, clade in enumerate(major_clade_counts):
			if(rtg_file[:2].lower() == clade[0]):
				major_clade_counts[c][1] += 1
				
	print(major_clade_counts)
						
	######### Calculating percentage of total species in each cell ###########
	
	lines_to_keep = []
	for l, line in enumerate(open(spreadsheet_to_filter, 'r')):
		if(l != 0):
			keep_line = True
			cells = line.split(',')
			og = cells[0]
			cells.pop(0);cells.remove('\n');
			for c, cell in enumerate(cells):
				if(cell != '' and cell != '\n'):
					if(c in indices_to_keep):
						if(float(cell) / float(major_clade_counts[c][1]) < threshold_one):
							keep_line = False
							break
					else:
						if(float(cell) / float(major_clade_counts[c][1]) > threshold_two):
							keep_line = False
							break
			if(keep_line == True):
				cells.insert(0, og)
				lines_to_keep.append(cells)
	
	return lines_to_keep
						
					
def main():

	#The three options of filters (which can be applied together) are the following:
		#Percent total species
		#No archaea
		#No bacteria
	
	major_clade_instances = get_major_clade_instances()
	
	new_lines = percent_total_species(major_clade_instances, threshold_one, threshold_two)
		
	with open(output_handle, 'w') as output_file:
		output_file.write(',')
		for clade in major_clade_instances:
			output_file.write(clade[0] + ',')
		output_file.write('\n')
		for line in new_lines:
			for entry in line:
				output_file.write(str(entry) + ',')
			output_file.write('\n')
	
	
main()	
					
					
					
					
					
					
					
					
					
					
					
					
					
					