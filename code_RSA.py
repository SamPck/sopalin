# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:44:43 2024

@author: samuel
"""


from random import randint
from sympy import randprime, gcd, mod_inverse
import matplotlib.pyplot as plt
import time

import mot_random


''' Chiffrement et déchiffrement '''

def encrypt(char_list, e, n):
    return [(pow(ord(c), e) - 1) % n  for c in char_list]
        
def decrypt(cypher_list, d, n):
    return [chr(97 + (nb**d)%n) for nb in cypher_list]
    



'''
# 3. Fonction de déchiffrement (liste de strings -> liste de caractères)
def decrypt(cipher_list, d, n):
    print(pow(int(26), d, n))
    return [chr(pow(int(c), d, n)) for c in cipher_list]



def codageRSA(t, p, q, e):
    n = p*q
    phi = (p-1)*(q-1)
    code = []
    for l in t:
        x = ord(l) - 97 # 97 correspond à 'a' en ASCII donc si l = 'a', x = 0
        code.append((x**e)%n)
    return code
'''



''' Décryptage '''

def inv_mod(a, r):
    for i in range(r):
        if (a*i)%r == 1:
            return i

def decryptageRSA(t, n, phi, e):
    #n = p*q
    #phi = (p-1)*(q-1)
    d = inv_mod(e, phi)
    msg = []
    for nb in t:
        msg.append(chr(97 + (nb**d)%n))
    return msg
        
'''
def generer_n(bits):
    # Bornes pour les nombres premiers
    low = 2**(bits - 1)
    high = 2**bits - 1
    
    # Génération de deux premiers distincts
    p = randprime(low, high)
    q = randprime(low, high)
    while q == p:
        q = randprime(low, high)
    
    n = p * q
    return n
'''

# Génère des valeurs utile de clé publique et privée aléatoirement pour simulations
def generate_rsa_keys(bits):
    lower = 2**(bits - 1)
    upper = 2**bits - 1
    p = randprime(lower, upper)
    q = randprime(lower, upper)
    while p == q:
        q = randprime(lower, upper)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e = randprime(3, phi)
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n), (p, q)


''' Factorisation de n '''

''' 1 - Méthode naive '''

def is_prime(p):
    if p==1:
        return False
    for d in range(2, int(p**0.5) + 1):
        if p % d == 0:
            return False
    return True

def facteurs(n):
    facteurs = []
    for p in range(2, int(n**0.5) + 1):
        if n % p == 0:
            facteurs.append(p)
            while n % p == 0:
                n //= p
    if n > 1:
        facteurs.append(n)
    return facteurs
    
def phi(n):
    res = n
    fact = facteurs(n)
    for p in fact:
        res *= (1- 1/p)
    return int(res)


def mth_naive(t, n, e):
    d = inv_mod(e, phi(n))
    msg = []
    for nb in t:
        msg.append(chr(97 + (nb**d)%n))
    return msg






# Temps pris pour obtenir phi(n)
def tps_calcul(n):
    t1 = time.time()
    p = phi(n)
    t2 = time.time()
    return t2-t1

def trace():
    bits_list = list(range(18, 21))
    N = [generate_rsa_keys(bits)[0][1] for bits in bits_list]
    T = [tps_calcul(n) for n in N]
    plt.plot(bits_list, T)
    plt.xlabel("Nombre de bits de $n$")
    plt.ylabel("Temps pris pour calculer " + r"$\varphi(n)$" + " (en sec)")
    plt.title("Efficacité temporelle de la méthode naïve")
    plt.show()



''' 2 - Algorithme rho de Pollard '''


# Récupération d'un facteur de n par algorithme de pollard rho
def pollard_rho(n):
    if n % 2 == 0:
        return 2  # cas rapide si N est pair
    def f(x):
        return (x * x + 1) % n

    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    if d == n:
        return None
    return d


# Simulation d'une attaque par pollard rho
def attaque_pollard(cipher_list, e, n):
    p = pollard_rho(n)
    if not p:
        return None
    q = n//p
    phi = (p-1)*(q-1)
    try:
        d = mod_inverse(e, phi)
    except ValueError:
        return None
    try:
        decrypted = decrypt(cipher_list, d, n)
    except:
        return None
    return decrypted


def est_decrypte(msg, bits):
    public, _, _ = generate_rsa_keys(bits)
    e, n = public
    cipher = encrypt(msg, e, n)
    return msg == attaque_pollard(cipher, e, n)


    
    
''' Graphe du temps d'exécution '''

def temps_pollard(bits):
    public, _, _ = generate_rsa_keys(bits)
    e, n = public
    
    msg_length = randint(1, 26)
    msg = list(mot_random.generate_random_word(msg_length))
    cipher = encrypt(msg, e, n)
    
    t1 = time.time()
    res = attaque_pollard(cipher, e, n)
    t2 = time.time()
    return t2 - t1
    
def trace_time(min_bits, max_bits):
    times = []
    sizes = []
    for bits in range(min_bits, max_bits + 1):
        sizes.append(bits)
        times.append(temps_pollard(bits))
    plt.plot(sizes, times, marker='s')
    plt.xlabel("Nombre de bits de $n$")
    plt.ylabel("Temps d'exécution de l'attaque (en $s$)")
    plt.title("Temps d'exécution de Pollard rho en fonction du nombre de bits de $n$")
    plt.show()
    

       

''' taux de reussite '''

def rate_pollard(min_bits, max_bits, nb_iter):
    sizes = list(range(min_bits, max_bits + 1))
    rates = []
    
    for bits in sizes:
        success = 0
        for _ in range(nb_iter):
            msg_length = randint(1, 26)
            msg = list(mot_random.generate_random_word(msg_length))
            if est_decrypte(msg, bits):
                success += 1
        rates.append(success/nb_iter)
    
    return sizes, rates
    

def trace_rate(min_bits, max_bits, nb_iter):
    sizes, rates = rate_pollard(min_bits, max_bits, nb_iter)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, rates)
    plt.xlabel("Nombre de bits de n")
    plt.ylabel("Taux de réussite de l'attaque")
    plt.title("Taux de réussite de l'attaque Pollard rho en fonction du nombre de bits de $n$")
    plt.ylim(0, 1.05)
    plt.show()



'''
# Fonction Pollard Rho avec un nombre limité d'itérations
def pollard_rho_limited(n, max_iter=5000):
    if n % 2 == 0:
        return 2
    x = random.randrange(2, n)
    y = x
    c = random.randrange(1, n)
    d = 1
    f = lambda x: (pow(x, 2, n) + c) % n

    for _ in range(max_iter):
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
        if d != 1 and d != n:
            return d
    return None
'''

'''
# Fonction pour tester le taux de réussite selon la taille de N
def test_success_rate(min_bits=30, max_bits=100, attempts_per_bit=5):
    bit_sizes = list(range(min_bits, max_bits + 1))
    success_rates = []

    for bits in bit_sizes:
        successes = 0
        for _ in range(attempts_per_bit):
            p = randprime(2**(bits // 2 - 1), 2**(bits // 2))
            q = randprime(2**(bits // 2 - 1), 2**(bits // 2))
            while p == q:
                q = randprime(2**(bits // 2 - 1), 2**(bits // 2))
            n = p * q
            factor = pollard_rho_limited(n)
            if factor is not None and n % factor == 0:
                successes += 1
        success_rate = successes / attempts_per_bit
        success_rates.append(success_rate)

    return bit_sizes, success_rates
'''










