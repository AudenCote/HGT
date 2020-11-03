import os
import sys
import ast
import recursive_goodness


def findall(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)
        
        

input_tree_handle = '../Current/ba-am/'


for file in os.listdir(input_tree_handle):
	if('DS' not in file):
		indices = []
		for line in open(input_tree_handle + file, 'r'):
			indices.extend([(i, line[i + 77:i + 87]) for i in findall('Ba_cy_Prsp', line)])
			indices.extend([(i, line[i + 78:i + 88]) for i in findall('Ba_cy_Prsp', line)])
			indices.extend([(i, line[i + 79:i + 89]) for i in findall('Ba_cy_Prsp', line)])
		
		for idx in indices:
			print(idx)
			if(idx[1] == 'Ba_cy_Prsp'):
				line = line[0 : idx[0] + 76] + line[idx[0] + 153 :]
				break
				
				
		with open('../Current/no_duplicates/' + file, 'w') as o:
			o.write(line)



# 
# 	entries_to_write = []
# 	split_line = line.split(':')
# 	
# 	new_line = []
# 	numbers = []
# 	
# 	for i, e in enumerate(split_line):
# 		if(i > 0):
# 			try:
# 				numbers.append(e[:22])
# 			except:
# 				numbers.append(e[:2])
# 			try:
# 				new_line.append(e[22:])
# 			except:
# 				continue
# 		else:
# 			new_line.append(e)
# 
# 	new_line = ''.join(new_line)
# 	new_line = new_line.replace("(", "['")
# 	new_line = new_line.replace(")", "']")
# 	new_line = new_line.replace(",", "', '")
# 	new_line = new_line.replace("'[", "[")
# 	new_line = new_line.replace("]'", "]")
# 
# 	new_list = ast.literal_eval(new_line)
# 	
# 	filtered_list = recursive_goodness.work_magic(new_list)
# 	filtered_list = str(filtered_list)
# 	filtered_list = filtered_list.replace("'", "")
# 	filtered_list = filtered_list.replace("[", "(")
# 	filtered_chars = list(filtered_list.replace("]", ")"))
# 	
# 	output_chars = []
# 	paren_idx = 0
# 	counting = False
# 	og_countdown = 0
# 	for c, char in enumerate(filtered_chars):
# 		output_chars.append(char)
# 		if(char == 'O' and filtered_chars[c + 1] == 'G' and filtered_chars[c + 2] == '5' and filtered_chars[c + 3] == '_'):
# 			counting = True
# 		if(counting == True):
# 			if(og_countdown == 9):
# 				counting = False
# 				og_countdown = 0
# 				output_chars.append(':')
# 				output_chars.extend(list(numbers[paren_idx]))
# 				paren_idx += 1
# 			else:
# 				og_countdown += 1
# 			
# 		if(char == ')'):
# 			output_chars.append(':')
# 			output_chars.extend(list(numbers[paren_idx]))
# 			paren_idx += 1
# 			
# 	output_str = ''.join(output_chars)
# 	
# 	#NEED TO REMOVE EMPTY PARENS AND PUT ORGANISMS IN CORRECT ORDER, ALSO ACCOUNT FOR FACT THAT ORGANISMS ARE DELETED; THEIR CORRESPONDING NUMBER SEQUENCES MUST BE DELETED AS WELL.
# 				
# 	with open(output_tree_handle, 'w') as o:
# 		o.write(output_str)
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
	
			