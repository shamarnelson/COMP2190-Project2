
import random
import math
import hashlib
import time
import sys

def expMod(b,n,m):
	"""Computes the modular exponent of a number"""
	"""returns (b^n mod m)"""
	if n==0:
		return 1
	elif n%2==0:
		return expMod((b*b)%m, n/2, m)
	else:
		return(b*expMod(b,n-1,m))%m

def RSAencrypt(m, e, n): #(3)
    """Encryption side of RSA"""
    return expMod(m, e, n)

def RSAdecrypt(c, d, n): #(2)
	"""Decryption side of RSA"""
	return expMod(c,d,n)

def gcd_iter(u, v):
    """Iterative Euclidean algorithm"""
    while v:
        u, v = v, u % v
    return abs(u)

def ext_Euclid(m,n):
    """Extended Euclidean algorithm"""
    a = (1,0,m)
    b = (0,1,n)
    while True:
        if b[2] == 0: return a[2]
        if b[2] == 1: return int(b[1] + (m if b[1] < 0 else 0))
        q = math.floor(a[2]/float(b[2]))
        t = (a[0] - (q * b[0]), a[1] - (q*b[1]), a[2] - (q*b[2]))
        a = b
        b = t

def generateNonce():
	"""This method returns a 16-bit random integer derived from hashing the
	    current time. This is used to test for liveness"""
	hash = hashlib.sha1()
	hash.update(str(time.time()).encode('utf-8'))
	return int.from_bytes(hash.digest()[:2], byteorder=sys.byteorder)

def findE(phi, p, q):
	"""Method to find e given phi, p, and q"""
	"""while loop to increment e until it is relatively prime to phi"""
	e = 3
	while gcd_iter(e, phi) != 1 or gcd_iter(e,p) != 1 or gcd_iter(e,q) != 1:
		if phi%2==0:
			e += 2
		else:
			e += 1
	return e
	
def findE(phi):
	"""Method to randomly choose a good e given phi"""
	e = random.randint(3, phi)
	while gcd_iter(e, phi) != 1:
		e = random.randint(3, phi)
	return e

def genKeys(p, q):
	"""Generate n, phi(n), e, and d."""
	n = p * q
	phi = (p-1)*(q-1)
	#e = findE(phi, p, q)
	e = findE(phi)
	
	d = ext_Euclid(phi, e) #Using the extended Euclidean algorithm to compute d
	if (d < 0):
		d += phi
	print ("n = "+ str(n))
	print ("phi(n) = "+ str(phi))
	print ("e = "+ str(e))
	print ("d = "+ str(d))
	print
	return n, e, d	