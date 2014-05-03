"""

Number Theory Routines by Dr. Ramanathan

"""

from math import sqrt
from fractions import gcd
from numpy import *
from pylab import *
from matplotlib import *

# Fast version of the sieve that only filters multiples of
# primes up to sqrt(n).

def fastErat(n): 
	primes = []
	if n < 1: return(primes)
	
	testbnd = sqrt(n + 0.000001)
	nxtpr = 1

	lst = range(2,n+1)
	while (lst != []) and (nxtpr <= testbnd) :
		nxtpr = lst[0]
		primes.append(nxtpr)
		lst = filter(lambda x: (x%nxtpr), lst) 

	return(primes+lst)

# Fast exponentiation mod p

def modp(x,y,n):
	acc, s, t = 1, x, y
	
	while t != 0:
		if (t & 1) == 1: acc = (s*acc)%n
		t = t >> 1
		s = (s**2)%n

	return(acc)

# Factorial function

def fact(n):
	if n == 0: return(1)
	elif n == 1: return(1)
	elif n > 1: return(n*fact(n-1))

# Bezout's theorem

def bezout(a,b):
	if a<=0 or b<=0: return("Error") # a and b must be positive
	m = eye(2,dtype=integer)
	r0,r1 = a,b

	while r1 > 0:
		q, rnext = r0/r1, r0%r1
		m = matrix([[0,1],[1,-q]]) * m
		r0,r1 = r1,rnext

	return(r0,m[0])

# Lists pseudoprimes

def pseudoErat(n,a):
        if n <= 1: return([])
        lst = range(2,n+1)
        lst = filter(lambda x: modp(a,x-1,x)==1,lst)
        return(lst)

# Simple factorization

def simpleFac(n):
	plst = fastErat(int(sqrt(n)))
	m = n
	factors = []
	while plst != [] and m > 1:
		p0 = plst[0]
		while m%p0 == 0:
			factors.append(p0)
			m = m/p0
		plst = plst[1:]
	if m > 1: factors.append(m)	
	return(factors)

# Lists the units mod n

def units(n):
	if n < 1: return([])
        lst = range(1,n+1)
        lst = filter(lambda x: gcd(x,n)==1,lst)
        return(lst)

# Calculates Euler's tiotient function

def tiotient(n):
	return(len(units(n)))

# Calculates the order of a modulo n

def order(a,n):
	if gcd(a,n) > 1: return(0)
        x, a0 = a%n, a%n
        t = 1
        while x != 1:
		x = (a0*x)%n
                t += 1
	return(t)

# Calculates powers of a mod n (from 0 to phi(n) - 1)

def orbit(a,n):
	lst, phi, i, x = [1], tiotient(n), 1, 1
	while i < phi:
		i += 1
		x = (a*x)%n
		lst.append(x)
	return(lst)

# Calculates the primroots modulo n

def primroots(n):
        phi = tiotient(n)
        lst = units(n)
        lst = filter(lambda x: order(x,n) == phi, lst)
        return(lst)	

# Tests for quad. residues using Euler's Critereon.
# Warning p must be a prime!

def legendre(a,p): 
	if a%p == 0: return(0)
	if modp(a,(p-1)/2,p) == 1: return(1)
	else: return(-1)

def showOrders(n): 
	A = array([map(lambda x: order(x,n), range(0,n))])
	xticks([])
	yticks([])
	imshow(A,interpolation='nearest',aspect=n/5.0)
	print(A)

def showQuadRes(n):
	A = array([map(lambda x: legendre(x,n), range(0,n))])
	xticks([])
	yticks([])
	imshow(A,interpolation='nearest',aspect=n/5.0)
	print(A)
