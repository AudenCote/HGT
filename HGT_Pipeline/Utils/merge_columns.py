#Dependencies
import os
import sys


spreadsheet_to_filter = sys.argv[1]
output_handle = spreadsheet_to_filter[:-4] + '_fixed.csv'


new_lines = []
for l, line in enumerate(open(spreadsheet_to_filter, 'r')):
	if(l == 0):
		cells = line.split(',')
		cells.pop(8); cells.remove('\n');
		
		new_lines.append(cells)
	if(l != 0):
		cells = line.split(',')
		cells[7] = int(cells[7]) + int(cells[8])
		cells.pop(8); cells.remove('\n');
		
		new_lines.append(cells)
		
with open(output_handle, 'w') as output_file:
		for line in new_lines:
			for entry in line:
				output_file.write(str(entry) + ',')
			output_file.write('\n')
		
		
