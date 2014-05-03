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
        self.isomorphisms = []
        return None
        
    def GenerateData(self):
        if self.Groupcheck() == False: return False
        self.MakeOrders()
        if self.CyclicCheck() == True:
            self.MakeGenerators()

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
        self.isgroup = False
        Domain = self.Domain
        Operation = self.Operation
        InverseCheck = self.InverseCheck
        if not(self.ClosureCheck()):
            print("Set not closed. Not a group.")
            return False
        if not(self.AssocCheck()):
            print("Not associative.")
            return False
        self.identity = self.Identity()
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
        self.isgroup = True
        return True

    # Note: If we identified pairs of inverses in the parent group,
    # we could drastically cut down on the number of sublists to check
    # and forgo an inverse check
    def Subgroups(self):
        try: self.inverses
        except AttributeError: self.InverseCheck()
        # Getting the Power Set of the PAIRS OF INVERSES rather than elements
        # cuts down on 2^(len(Domain)/2) possibilities
        # which is way more cycles than sorting through all of them into lists of elements takes (i think)
        inversepowset = PowerSet(self.inverses)
        possible_subgroups = []
        for n in inversepowset:
            temp = []
            temp.append(self.identity)
            for pair in n:
                if pair[0] == pair[1]: temp.append(pair[0])
                else:
                    temp.append(pair[0])
                    temp.append(pair[1])
            possible_subgroups.append(temp)
        #print(subsets)
        if len(possible_subgroups) < 1: return []
        subgroups = []
        try: self.identity
        except AttributeError: self.Identity()
        for n in possible_subgroups:
            a = BinaryGroup(n,self.Operation)
            # Obviously we don't need to check associativity
            # 2. There's no way to get around closure check that I know of :(
            if not a.ClosureCheck(): continue
            a.isgroup = True
            subgroups.append(a)
        self.subgroups = subgroups
        return subgroups

    def ClosureCheck(self):
        self.isclosed = False
        Domain = self.Domain
        Operation = self.Operation
        for n in Domain:
            for n1 in Domain:
                if (Operation(n,n1) in Domain):
                    pass
                else:
                    print("Operation( "+str(n)+" , "+str(n1)+" ) = "+str(Operation(n,n1))+"  Which is not in the Domain: "+printlist(Domain))
                    return False
        self.isclosed = True
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
                        self.isassoc = True
                        return True
            #print("Passed Associativity")
        self.isassoc = False
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
                self.identity = n
                return(n)
        # Returns string "False" because 0 is additive identity
        # and python interprets integer 0 as boolean value False
        # So we can use a string to clear up this confusion
        #print("No Identity")
        self.idenity = "False"
        return "False"


    def InverseCheck(self):
        Domain = self.Domain[:]
        Operation = self.Operation
        try: self.identity
        except AttributeError: self.Identity()
        identity = self.identity
        self.inverses = []
        Domain.remove(identity)
        for n in Domain:
            hasinverse = 0
            for n1 in Domain:
                if Operation(n,n1) == identity:
                    if ([n1,n]) not in self.inverses: self.inverses.append([n,n1])
                    hasinverse = 1
                    break
                else:
                    pass
            if hasinverse == 0:
                #print("Element: "+str(n)+" \n has failed inverse check")
                self.hasinverses = False
                return False
        #print("Inverses Exist!")
        self.hasinverses = True
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
                self.iscyclic = True
                return True
        self.iscyclic = False
        return False

    def MakeOrders(self):
        self.Orders = {str(n) : self.Order(n) for n in self.Domain}
        return self.Orders
    def MakeGenerators(self):
        Generators = []
        for n in self.Domain:
            if self.Order(n) == self.GroupOrder:
                Generators.append(n)
        self.Generators = Generators
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



# Binary represntation of range(0,len(set)) gives the power set
# in the set {a,b,c}, 100 = {a}, 010 = {b}, 101 = {a,c}, etc.
def PowerSet(inlist):
    outlist = []
    i = 0
    while i < 2**(len(inlist)):
        templist = []
        tempi = i
        for temppos in range(0,len(inlist))[::-1]:
            #Checks if the  bit on the right is a 1 or 0
            if i&1: templist.append(inlist[temppos])
            #i eliminates a bit on the right
            tempi>>=1
        i += 1
        outlist.append(templist)
    return outlist

def ListMapFunc(OrderedDomain, OrderedRange, element):
    if OrderedDomain.count(element) != 1: return False
    return OrderedRange[OrderedDomain.index(element)]
