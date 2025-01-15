# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:44:43 2024

@author: samuel
"""

p = 11
q = 23
c = 9
m = (p-1)*(q-1) #220
n = 253

t = ['s', 'a', 'm', 'u', 'e', 'l']

def codageRSA(t, n, c):
    code = []
    for l in t:
        x = ord(l) - 97
        code.append((x**c)%n)
    return code


def inv_mod(a, r):
    for i in range(r):
        if (a*i)%r == 1:
            return i
        
def decodageRSA(p, q, c, code):
    d = inv_mod(c, m)
    msg = []
    for nb in code:
        msg.append(chr(97 + (nb**d)%n))
    return msg
    
