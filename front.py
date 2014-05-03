from permutations import *
from groups import *
# This file should have functions which take string input and
# put it in a format to be handled by permutations.py and groups.py
# and then return answers which are pretty and readable
# the actual GUI programming should be in gui.py

# String to permutation
# input string should be of the form '(12)(12)' or '(1,2)(1,2)'
# we want to output in the form perm([cycle([1,2]),cycle([1,2])])
def str2perm(string):
	cycles = string.count('(')
	if cycles != string.count(')'):
		print("Error: parenthesis mismatch. (: "+ str(cycles)+" and ): "+ str(string.count(')')))
		return None
	usecommas = ',' in string #checks if elements are comma separated
	cyclelist = []
	tempstring = string[:]
	for unusedcounter in range(0,cycles):
		tempcycle = []
		if usecommas:
			tempcycle = [ (tempstring[tempstring.index('(')+1]) ]
			while (',' in tempstring) and (tempstring.index(',') < tempstring.index(')')):
				tempcycle.append( tempstring[tempstring.index(',')+1] )
				tempstring = tempstring[tempstring.index(',')+1:]
			tempstring = tempstring[tempstring.index(')')+1:]
		else:
			tempstring = tempstring[tempstring.index('(')+1:]
			while tempstring[0] != ')':
				tempcycle.append(tempstring[0])
				tempstring = tempstring[1:]
		cyclelist.append(cycle(tempcycle))
	return permutation(cyclelist)
		
		
		
