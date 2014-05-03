from permutations import *
from examples import *

def printlist(inlist):
    outlist = []
    for n in inlist: outlist.append(str(n))
    return str(outlist)

class BinaryGroup():
    def __init__(self, Domain, Operation):
        self.Domain = Domain
        self.GroupOrder = len(Domain)
        self.Operation = Operation
        Domain = self.Domain
        Operation = self.Operation
        self.identity = self.Identity()
        self.isgroup = self.GroupCheck()
        self.iscyclic = self.CyclicCheck()
        self.Orders = self.MakeOrders()

        # Generating subgroups in initialization generates the recursively,
        # which SHOULD be fine, but infinitely loops for some reason
        #self.Subgroups = self.GenerateSubgroups()

        #Any time an __eq__ check returns true, we add the other group to the
        # first slot of a tuple and the mapping to the second slot
        self.isomorphisms = []

        if self.iscyclic == True:
            self.Generators = self.MakeGenerators()
        return None

    #Equality test should return True if two groups are isomorphic
    #Only working for cyclic groups right now
    def __eq__(self, other):
        if (self.iscyclic and other.iscyclic and self.GroupOrder == other.GroupOrder):
            return True
        range_perms = permutelist(other.Domain)[1:]
        for OrderedRange in range_perms:
            if self.IsomorphismCheck(other,self.Domain,OrderedRange):
                self.isomorphisms.append( (other, OrderedRange) )
                return True
        return False
    def __neq__(self, other): return not self == other

    def printiso(self, OtherGroup):
        if self == OtherGroup:
            for n in self.isomorphisms:
                if n[0] == OtherGroup:
                    for i in range(0,len(n[1])):
                        print( str(self.Domain[i])+" to "+str(n[1][i]) )
                    return None
            print("Something went wrong")
            return None
        else:
            print("No Isomorphism")
            return False


    #Less than (<) test should return true if self is a subgroup of other
    #We could define this the conventional way,
    #but we'd like to have support for being isomorphic to a subgroup
    def __lt__(self,other):
        if self.Operation != other.Operation: return False
        if not other.isgroup: return False
        for n in self.Domain:
            if n not in other.Domain: return False
        if self.ClosureCheck(): return True
        else: return False

    #self > other
    def __gt__(self,other):
        if self.Operation != other.Operation: return False
        if not self.isgroup: return False
        for n in other.Domain:
            if n not in self.Domain: return False
        if other.ClosureCheck(): return True

    #leq and geq do not support isomorphisms to be consistent with > and <.
    def __le__(self,other):
        if (self < other) or (self.Domain == other.Domain): return True
        else: return False
    def __ge__(self,other):
        if (self > other) or (self.Domain == other.Domain): return True

	# Addition yeilds Direct External Product
    def __add__(self, other):
    	l = [self.Operation, other.Operation]
    	f = DirectExternalProduct(l)
    	NewDomain = []
    	for element1 in self.Domain:
    		for element2 in other.Domain:
    			NewDomain.append([element1,element2])
    	return BinaryGroup(NewDomain, f.CompOperation)

	# Needs error handling incase operation isn't defined for object input
	def lcoset(self,element):
		NewDomain = []
		for n in self.Domain:
			NewDomain.append(self.Operation(element,n))
		return BinaryGroup(NewDomain,self.Operation)
	
	def rcoset(self,element):
		NewDomain = []
		for n in self.Domain:
			NewDomain.append(self.Operation(n,element))
		return BinaryGroup(NewDomain,self.Operation)

    def GroupCheck(self):
        identity = False
        Domain = self.Domain
        Operation = self.Operation
        InverseCheck = self.InverseCheck
        if not(self.ClosureCheck()):
            print("Set not closed. Not a group.")
            return False
        if not(self.AssocCheck()):
            print("Not associative.")
            return False
        identity = self.Identity()
        # Identity function uses the string "False"
        # in case we have identity = the integer 0
        # which is equivalent to bool False
        if identity == "False":
            print("No identity in Set: "+printlist(self.Domain))
            return False
        if not(InverseCheck()):
            print("Incomplete Inverses.")
            return False
        # print(printlist(self.Domain)+" under "+str(self.Operation)+" Is a group!")
        return True

    def Subgroups(self):
        subsets = GenerateSublists(self.Domain)
        #print(subsets)
        if len(subsets) < 1: return []
        subgroups = []
        for n in subsets:
            a = BinaryGroup(n,self.Operation)
            if a.isgroup: subgroups.append(a)
        a.subgroups = subgroups
        return subgroups

    def ClosureCheck(self):
        Domain = self.Domain
        Operation = self.Operation
        for n in Domain:
            for n1 in Domain:
                if (Operation(n,n1) in Domain):
                    pass
                else:
                    print("Operation( "+str(n)+" , "+str(n1)+" ) = "+str(Operation(n,n1))+"  Which is not in the Domain: "+printlist(Domain))
                    return False
        return True

    def AssocCheck(self):
        Domain = self.Domain
        Operation = self.Operation
        for n in Domain:
            for n1 in Domain:
                for n2 in Domain:
                    a = Operation(  Operation(n,n1)  ,  n2  )
                    b = Operation(  n  ,  Operation(n1,n2)  )
                    if (a == b):
                        return True
            #print("Passed Associativity")
        return False

    #This one returns the identity so that you can keep track of it
    #If there is no identity, it returns False
    def Identity(self):
        Domain = self.Domain
        Operation = self.Operation
        for n in Domain:
            nident = 1
            for n1 in Domain:
                if (Operation(n,n1) == n1):
                    pass
                else:
                    nident = 0
                    #print(str(n)+" is not the identity")
                    #print("Operation( "+str(n)+" , "+str(n1)+ " ) = "+str(Operation(n,n1)))
                    break
            if nident == 1:
                return(n)
        # Returns string "False" because 0 is additive identity
        # and python interprets integer 0 as boolean value False
        # So we can use a string to clear up this confusion
        #print("No Identity")
        return "False"


    def InverseCheck(self):
        Domain = self.Domain
        Operation = self.Operation
        identity = self.identity
        for n in Domain:
            hasinverse = 0
            for n1 in Domain:
                if Operation(n,n1) == identity:
                    hasinverse = 1
                    break
                else:
                    pass
            if hasinverse == 0:
                #print("Element: "+str(n)+" \n has failed inverse check")
                return False
        #print("Inverses Exist!")
        return True

    def IsomorphismCheck(self,OtherGroup,OrderedDomain,OrderedRange):
        f = ListMapFunc
        for n in OrderedRange:
            if OrderedRange.count(n) != 1:
                print("Malformed Range")
                return False
        #ListMapFunc already gives that the mapping is a bijection
        #Only need to check Operation Preservation
        #for a,b in Domain, f(ab) = f(a)f(b)
        for a in OrderedDomain:
            for b in OrderedDomain:
                if f(OrderedDomain,OrderedRange,self.Operation(a,b)) != OtherGroup.Operation(f(OrderedDomain,OrderedRange,a),f(OrderedDomain,OrderedRange,b)): return False
        return True

    def CyclicCheck(self):
        Domain = self.Domain
        Operation = self.Operation
        identity = self.identity
        for n in Domain:
            npower = n
            order = 1
            while npower != identity:
                npower = Operation(npower,n)
                order += 1
                #Incase order = infinity
                if order > len(Domain):
                    break
            if order == len(Domain):
                return True
        return False

    def MakeOrders(self):
        return {str(n) : self.Order(n) for n in self.Domain}
    def MakeGenerators(self):
        Generators = []
        for n in self.Domain:
            if self.Order(n) == self.GroupOrder:
                Generators.append(n)
        return Generators

    #An output of 0 means order infinity
    def Order(self, n):
        order = 1
        npower = n
        while npower != self.identity:
            npower = self.Operation(npower, n)
            order += 1
            if order > self.GroupOrder:
                return 0
        return order

    def CyclicGroup(self, n):
        if n not in self.Domain:
            return False
        cycle = []
        npower = n
        while npower not in cycle:
            cycle.append(npower)
            npower = self.Operation(npower, n)
        return BinaryGroup(cycle,self.Operation)



#Some helper functions which don't necessarily belong in the BinaryGroup class

def sublistcheck(one,other):
    for n in other:
        if n not in one: return False
    return True

# CompOperation is componentwise operation, input an ordered list of operations
# to apply to elements which should be a list of elements
class DirectExternalProduct():
	def __init__(self,OrderedOperationList):
		self.Oplist = OrderedOperationList
	def CompOperation(self,tupelement1,tupelement2):
		if len(tupelement1) != len(tupelement2) or len(tupelement1) != len(self.Oplist):
			print("Direct External Product Input Size Mismatch")
			return False
		outlist = [self.Oplist[n]( tupelement1[n], tupelement2[n] ) for n in range(0,len(self.Oplist))]
		return outlist




def GenerateSublists(inlist):
    outlist = [inlist]
    if len(inlist) < 2: return []
    for level in range(0,len(inlist)):
        a = inlist[:]
        a.remove(a[level])
        chunk = GenerateSublists(a)
        for n in chunk: outlist.append(n)
    return remdup(outlist)

def ListMapFunc(OrderedDomain, OrderedRange, element):
    if OrderedDomain.count(element) != 1: return False
    return OrderedRange[OrderedDomain.index(element)]
