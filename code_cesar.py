# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:31:22 2024

@author: samuel
"""
# a = 97, z = 122 en ASCII

tab = ['a', 'v', 'e', 'c', 'e', 's', 'a', 'r']
tab2 = ['e', 'l', 'e', 'p', 'h', 'a', 'n', 't']


def codageCesar(t, d):
    for i in range(len(t)):
        if ord(t[i]) - d >= 97:
            t[i] = chr(ord(t[i]) - d)
        else:
            t[i] = chr(122 - (97 - (ord(t[i]) - d)) + 1)
    return t
    
cod = codageCesar(tab2, 4)

def decodageCesar(t, d):
    for i in range(len(t)):
        if ord(t[i]) + d <= 122:
            t[i] = chr(ord(t[i]) + d)
        else:
            t[i] = chr(97 + (ord(t[i]) + d - 122) - 1)
    return t
    

def frequences(t):
    return {chr(i) : t.count(chr(i)) for i in range(97, 123)}

def decodageAuto(t):
    occ = frequences(t)
    max_occ = max(occ.values())
    for k in occ:
        if occ[k] == max_occ:
            d = abs(ord('e') - ord(k))
            return decodageCesar(t, d)
        
t = 'nvpr'