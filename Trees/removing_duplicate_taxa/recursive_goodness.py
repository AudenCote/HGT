import ast

vals = []

def work_magic(l):
    sublists = []
    pops = []
    
    for i in range(len(l)):
        if type(l[i]) == list:
            sublists.append(l[i])
            pops.append(i)
    
    for i in range(len(pops), 0, -1):
        l.pop(pops[i-1])
        
    l = list(dict.fromkeys(l))
    temp = []
    for val in l:
    	if val not in vals:
    		temp.append(val)
    		vals.append(val)
    l = temp
    
    for i in sublists:
        l.append(work_magic(i))
                
    return l
		
	



















