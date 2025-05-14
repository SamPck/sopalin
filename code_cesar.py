# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:31:22 2024

@author: samuel
"""
# a = 97, z = 122 en ASCII

tab = ['a', 'v', 'e', 'c', 'e', 's', 'a', 'r']
tab2 = ['e', 'l', 'e', 'p', 'h', 'a', 'n', 't']

def codageCesar(t, d): # d >= 0
    t_bis = t[:]
    for i in range(len(t)):
        if ord(t[i]) + d <= 122:
            t_bis[i] = chr(ord(t[i]) + d)
        else:
            t_bis[i] = chr(97 + (ord(t[i]) + d) % 122 - 1)
    return t_bis
    
cod = codageCesar(tab2, 4)

def decodageCesar(t, d):
    t_bis = t[:]
    for i in range(len(t)):
        if ord(t[i]) - d >= 97:
            t_bis[i] = chr(ord(t[i]) - d)
        else:
            t_bis[i] = chr(122 - (97 - (ord(t[i]) - d)) + 1)
    return t_bis
    

def frequences(t):
    return {chr(i) : t.count(chr(i)) for i in range(97, 123)}

def decodageAuto(t):
    occ = frequences(t)
    max_occ = max(occ.values())
    for k in occ:
        if occ[k] == max_occ:
            d = abs(ord('e') - ord(k))
            return decodageCesar(t, d)
        
'''
FAIRE GRAPHE QUI MONTRE COMMENT EVOLUE LA FAIT DE TROUVER LE MOT EN FONCTION
DE LA TAILLE DU MOT POUR DES MOTS ALEATOIRE DANS LA LANGUE FR
'''

import mot_random

import matplotlib.pyplot as plt
import numpy as np 



def mth_intel(N_min, N_max, m):
    # Determiner le nombre de reussite de la fonction decodageAuto sur m essais 
    # pour un mot de longueur comprise entre N_min et N_max
    length = [N for N in range(N_min, N_max+1)]
    sucess = []
    for N in range(N_min, N_max+1):
        count = 0
        for i in range(m):
            mot = mot_random.generate_random_word(N)
            if mot != 'None':
                lst_mot = [char for char in mot]    
                d = np.random.randint(0, 25)
                mot_chiffre = codageCesar(lst_mot, d)
                mot_decrypte = decodageAuto(mot_chiffre)
                if mot_decrypte == lst_mot:
                    count += 1
        sucess.append(count)
        
    # Représentation graphique  
    plt.plot(length, sucess)
    plt.xlabel("Longueur du mot")
    plt.ylabel("Nombre de succès sur {} essais".format(m))
    plt.title("")
    plt.show()
    plt.savefig("mth_intel.png")

    
import pandas as pd

def mth_brut(m):   
    colonnes = {}
    for i in range(m):
        
        # Génère un mot de longueur aléatoire entre 2 et 12
        N = np.random.randint(2, 12)
        mot =  mot_random.generate_random_word(N)
        
        lst_mot = [char for char in mot]
        d = np.random.randint(0, 25)
        mot_chiffre = codageCesar(lst_mot, d)
        
        # Déchiffre avec tous les décalages possibles 
        decryptages_possibles = []
        for p in range(26):
            decryptages_possibles.append("".join(decodageCesar(mot_chiffre, p)))
            
        if mot not in colonnes.keys():
            colonnes[mot] = decryptages_possibles
        
    # Transformer le dictionnaire en DataFrame
    df = pd.DataFrame(colonnes)
    
    # Exporter vers un fichier Excel
    df.to_excel('mth_brut.xlsx', index=False)
    
        
   
