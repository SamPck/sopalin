# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 17:02:50 2024

@author: samuel
"""

# a = 97, z = 122 en ASCII

p = 19
q = 23
B = 100
n = p*q #437

def cryptage(t):
    code = []
    for l in t:
        nb = abs(ord(l) - 97)
        code.append((nb * (nb + B))%n)
    return code 