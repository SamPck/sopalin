# -*- coding: utf-8 -*-
"""
Created on Mon May 12 09:43:27 2025

@author: samue
"""

import pandas as pd
import random
import re

def get_file():
    # Charger le fichier XLSB une seule fois
    fichier_xlsb = 'Lexique383.xlsb'
    df = pd.read_excel(fichier_xlsb, engine='pyxlsb')
    
    # Sauvegarder le DataFrame en Pickle
    df.to_pickle('Lexique383.pkl')

def generate_random_word(N):
    # Charger le fichier Pickle
    df = pd.read_pickle('Lexique383.pkl')
    # Filtrer les mots qui ont exactement la longueur choisie
    df_filtree = df[(df['15_nblettres'] == N) & (df['1_ortho'].notna())]
    
    # Transformer les mots filtrés en une liste et retirer les caractères spéciaux
    mots = df_filtree['1_ortho'].astype(str).tolist()
    mots_sans_accents = [mot for mot in mots if re.fullmatch(r'[a-z]+', mot)]
    
    # Choisir un mot aléatoire
    if mots_sans_accents:
        mot_aleatoire = random.choice(mots_sans_accents)
        return mot_aleatoire
    else:
        return 'None'


