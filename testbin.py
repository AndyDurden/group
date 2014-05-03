TEST CHANGE HAHAHALKHDSFASJDF;LKDSAJFDSAF
ASDLKFJLSAJFD
DSAF
SAD
FDSA
F
DSAF
DSAG
DSAG
DSAF
SADG
EW
GFW

# We want a function which will take a list, and output a list of all possible sublists.

#check if OTHER is a sublist of SELF
def sublistcheck(one,other):
	for n in other:
		if n not in one: return False
	return True
	
def remdup(inlist):
	out = []
	for n in inlist:
		if n not in out:
			out.append(n)
	return out
	
def GenerateSublists(inlist):
	outlist = [inlist]
	for level in range(0,len(inlist)):
		a = inlist[:]
		a.remove(a[level])
		chunk = GenerateSublists(a)
		for n in chunk: outlist.append(n)
	return remdup(outlist)

#We want a better way to generate the powerset.


# Binary represntation of range(0,len(set)) gives the power set
# in the set {a,b,c}, 100 = {a}, 010 = {b}, 101 = {a,c}, etc.
def PowerSet(inlist):
	outlist = []
	for i in range(0,2**len(inlist)):
		templist = []
		for temppos in range(0,len(inlist)-1)[::-1]:
			#Checks if the  bit on the right is a 1 or 0
			if i&1: templist.append(inlist[temppos])
			#i eliminates a bit on the right
			i>>=1
		outlist.append(templist)
	return outlist
		
	
