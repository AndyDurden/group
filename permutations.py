#Helper Functions

def remdup(inlist):
    out = []
    for n in inlist:
        if n not in out:
            out.append(n)
    return out


#input is a list (mathematically a product) of cycles, like [ [1,2], [3,4] ]
#Represented mathematically as (12)(34)



class permutation():
	def __init__(self, cyclelist):
		self.input = cyclelist
		self.disjoint = self.disjoint(self.input)
		return None
		
	def __str__(self):
		outstring = ''
		for n in self.disjoint:
			outstring = outstring + str(n)
		return outstring
		
	def __repr__(self):
		return str(self)
	
	def __eq__(self, other):
		if other.__class__.__name__ != 'permutation': return False
		if len(self.disjoint) != len(other.disjoint): return False
		for cycle in self.disjoint:
			unionbool = 0
			for cycle1 in other.disjoint:
				if cycle == cycle1:
					unionbool = 1
					break
			if unionbool == 0:
				return False
		return True
		
	def __ne__(self,other):
		return not self.__eq__(other)
				
	def disjointcheck(self,cyclelist):
		for n in cyclelist:
			same = 1
			for n1 in cyclelist:
				if n == n1 and same == 1:
					#requires same check incase cyclelist = [(12), (12)] (not disjoint)
					same = 0
					continue #skips check
				if set(n.cycle).intersection(set(n1.cycle)):
					return False
		return True
	
	#Gives permutation's action on an element. p = (12)(34), p.func(1) = 2.
	#We use disjoint as the map, but this algo will work for any perm.
	def func(self, element):
		tempelement = element
		for n in (range(0,len(self.disjoint))[::-1]):
			tempelement = self.disjoint[n].func(tempelement)
	
	#This is the big algo here.
	#Input a permutation as a product of cycles
	#Output is a perm as a product of DISJOINT cycles
	#This result is unique, so always use it to check perm. equality!
	def disjoint(self, inl):
		#if self.disjointcheck(inl): return inl
		elementset = []
		for n in inl:
			elementset = list(set(elementset).union(set(n.cycle)))
		writtenelements = set([])
		returnperm = []
		firstrun = 1
		for element in elementset:
			#skips loop if we already wrote that element
			if element in writtenelements: continue
			else:
				tempelement = None
				startcycle=1
				#Loops over until we finish the cycle (we get element back)
				while tempelement != element:
				#While cond. stops loop once we get back to our input element
					if startcycle == 1:
						tempcycle = cycle([])
						tempelement = element
						startcycle = 0
					tempcycle.cycle.append(tempelement)
					writtenelements.add(tempelement)
					#Right to left through every cycle
					for n in (range(0,len(inl))[::-1]):
						tempelement = inl[n].func(tempelement)
				if len(tempcycle.cycle) != 1: #Removes 1-cycles
					returnperm.append(tempcycle)
		#Removes duplicates (usually extra identities)
		returnperm = remdup(returnperm)
		#Removes identities accompanying non-trivial cycles
		if (len(returnperm) > 1) and (cycle_e in returnperm): returnperm.remove(cycle_e) 
		#Makes sure we have at least one cycle (if empty, the identity)
		if len(returnperm) == 0: returnperm = [cycle([])]
		return returnperm


	#Multiplication on the left, other * self
	def __mul__(self, other):
		#Hotfix to pass identity
		if self == perm_e: return other
		if other == perm_e: return self
		#the [:] creates a copy rather than assigning inperm to other.disjoint
		inperm = other.disjoint[:]
		inperm.extend(self.disjoint)
		return permutation(inperm)
	#Multiplication on the right, self * other
	def __rmul__(self, other):
		if self == perm_e: return other
		if other == perm_e: return self
		inperm = self.disjoint[:]
		inperm.extend(self.other)
		return permutation(self.disjoint)
	


#input is a list of elements, like [1,2,3,4]
class cycle():
	def __init__(self, cyclelist):
		for n in cyclelist:
			if cyclelist.count(n) > 1:
				print("Error: Malformed Cycle")
				return False
		if len(cyclelist) == 1: cyclelist = []
		self.cycle = cyclelist
		return None
		
	def __str__(self):
		if self.cycle == []: return "()"
		outstr = '('
		for n in self.cycle:
			outstr = outstr + str(n) + ","
		outstr = outstr[:len(outstr)-1] + ')' #overwrites last comma
		return(outstr)
		
	def __repr__(self):
		return str(self)
		
	#Checks equality by rotating
	def __eq__(self, other):
		if other.__class__.__name__ != 'cycle': return False
		if self.cycle == other.cycle:
			return True
		if len(self.cycle) != len(other.cycle):
			return False
		temp = self.cycle
		for n in range(1,len(self.cycle)):
			temp = rotatelist(temp)
			if temp == other.cycle:
				return True
		return False
	def __ne__(self,other):
		return not(self == other)

	#Returns cycle's action on an element c = (12), c.func(1) = 2
	def func(self,element):
		if element in self.cycle:
			return self.cycle[(self.cycle.index(element)+1) % len(self.cycle)]
		else:
			return element



def rotatelist(cycle):
    rotatedcycle = cycle[:]
    for element in cycle:
        rotatedcycle[(cycle.index(element)+1) % len(cycle)] = cycle[ (cycle.index(element))]
    return rotatedcycle
    
    

#We want to generate every possible permutation on a domain
#Note that the output has an empty list in slot 0, this is necessary for the recursion to work
def permutelist(domain):
	outlist = [[]]
	for element in domain:
		reduced_domain = domain[:]
		reduced_domain.remove(element)
		for n in permutelist(reduced_domain): 
			n.insert(0,element)
			if len(n) == len(domain):
				outlist.append(n)
	return outlist
									

#Input two lists and they will be constructed as a permutation mapping OrderedDomain[n] to OrderedRange[n]
def mapping2perm(OrderedDomain, OrderedRange):
	#Hotfix to pass identity
	if OrderedDomain == [] or OrderedRange == []: return permutation( [ cycle([]) ] )
	#First we must check if the mapping is a bijection. It suffices to check if every member is accounted for
	if len(OrderedDomain) != len(OrderedRange):
		return False
	if max(map(OrderedDomain.count, OrderedDomain)) > 1:
		return False
	for n in OrderedDomain:
		if n not in OrderedRange:
			return False
	#After these checks we know we can create a product of permutations
	cyclelist = []
	elimset = OrderedDomain[:]
	for startelement in OrderedDomain:
		if startelement not in elimset: continue
		tempcycle = []
		tempelement = None
		firstrun = 1
		while tempelement != startelement:
			if firstrun == 1:
				tempelement = startelement
				firstrun = 0
			tempcycle.append(tempelement)
			elimset.remove(tempelement)
			tempelement = OrderedRange[OrderedDomain.index(tempelement)]
		cyclelist.append(cycle(tempcycle))
	return permutation(cyclelist)
			
cycle_e = cycle([])			
perm_e = permutation( [ cycle_e ] )
		
		
		
		
		
		
		
