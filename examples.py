#regular ol' functions.
from permutations import *
from front import *

class mod():
    def __init__(self, modulus):
        self.modulus = modulus
    def add(self,a,b):
        return (a+b)%self.modulus
    def mult(self,a,b):
        return (a*b)%self.modulus



def addition(a,b):
    return (a+b)
modulus = 6
def modaddition(a,b):
    return (a+b)%modulus
def multiplication(a,b):
    return (a*b)
def modmultiplication(a,b):
    return (a*b)%modulus


#Some built-in sets
z = [ range(0,i-1) for i in range(1,20) ]
unitsmod6 = [1,2,3,4,5]


# Permutations can be created in two ways:
# 1. Directly calling them and their composing cycles like we have for D4
# 2. Using the str2perm('string') function with an argument of form '(123)(234)' or '(1,2,3)(2,3,4)'

# Here we'll construct D4, which is a group under
# composition of it's functions
R0 = permutation([])
R90 = permutation([cycle([1,2,3,4])])
R180 = permutation([cycle([1,3]),cycle([2,4])])
R270 = permutation([cycle([1,4,3,2])])
H = permutation([cycle([1,4]),cycle([2,3])])
V = permutation([cycle([1,2]),cycle([3,4])])
LD = permutation([cycle([1,3])])
RD = permutation([cycle([4,2])])


R4 = [R0, R90, R180, R270]
D4 = [R0, R90, R180, R270, H, V, LD, RD]

#Permutation groups!
#Since my code isn't very efficient, permutation groups larger than S5 take a while to generate.
#Furthermore, checking if S4 == S4 takes so long that python kills on my pc
#S3 == S3 is quick though.
PermGroupUpperLimit = 5
PermGroup = {'S'+str(i) : [mapping2perm(range(1,i+1),x) for x in permutelist(range(1,i+1))[1:]] for i in range(1,PermGroupUpperLimit+1)}

