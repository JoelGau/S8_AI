#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:24:04 2020

@author: Laurent Colas
"""

import numpy as np
import GA_module as ga

# Alternance des gènes
def sexyTime_first(p1,p2):
    gr2 = p1.gr2
    gr4 = p1.gr4
    gr6 = p1.gr6
    aav = p1.aav
    
    gr3_2 = p2.gr3
    gr5_2 = p2.gr5
    rdiff_2 = p2.dgr
    aar_2 = p2.aar
    
    p1.gr3 = gr3_2
    p1.gr5 = gr5_2
    p1.dgr = rdiff_2
    p1.aar = aar_2
    
    p2.gr2 = gr2
    p2.gr4 = gr4
    p2.gr6 = gr6
    p2.aav = aav

    
    return (p1, p2)
    

# Enfant maximum et enfant Minimum
def sexyTime_minmax(p1,p2):
    gear2ratio = find_big(p1.gr2, p2.gr2)
    gear3ratio = find_big(p1.gr3, p2.gr3)
    gear4ratio = find_big(p1.gr4, p2.gr4)
    gear5ratio = find_big(p1.gr5, p2.gr5)
    gear6ratio = find_big(p1.gr6, p2.gr6)
    reardifferentialratio = find_big(p1.dgr, p2.dgr)
    rearspoilerangle = find_big(p1.aav, p2.aav)
    frontspoilerangle = find_big(p1.aar, p2.aar)
    
    p1.gr2 = gear2ratio
    p1.gr3 = gear3ratio
    p1.gr4 = gear4ratio
    p1.gr5 = gear5ratio
    p1.gr6 = gear6ratio
    p1.dgr = reardifferentialratio
    p1.aav = rearspoilerangle
    p1.aar = frontspoilerangle
    
    gear2ratio = find_small(p1.gr2, p2.gr2)
    gear3ratio = find_small(p1.gr3, p2.gr3)
    gear4ratio = find_small(p1.gr4, p2.gr4)
    gear5ratio = find_small(p1.gr5, p2.gr5)
    gear6ratio = find_small(p1.gr6, p2.gr6)
    reardifferentialratio = find_small(p1.dgr, p2.dgr)
    rearspoilerangle = find_small(p1.aav, p2.aav)
    frontspoilerangle = find_small(p1.aar, p2.aar)
    
    p2.gr2 = gear2ratio
    p2.gr3 = gear3ratio
    p2.gr4 = gear4ratio
    p2.gr5 = gear5ratio
    p2.gr6 = gear6ratio
    p2.dgr = reardifferentialratio
    p2.aav = rearspoilerangle
    p2.aar = frontspoilerangle
    
def sexy_time3(p1,p2,nb_premier = 3):
    kid1 = {}
    kid2 = {}
    i = 0
    for key in p1.keys():
        if i < nb_premier:
            kid1[key] = p1[key]
            kid2[key] = p2[key]
        else:
            kid1[key] = p2[key]
            kid2[key] = p1[key]
        i+=1
        
    return (kid1, kid2)

def find_big(num1, num2):
    if (num1 >= num2):
        return num1
    else:
        return num2
    
def find_small(num1, num2):
    if (num1 <= num2):
        return num1
    else:
        return num2
    
def float_to_bin(individu):
    bin_gear_2 = float_bin(individu['gear-2-ratio'][0],1)
    print(bin_gear2)
    
def float_bin(number, places = 1):
    whole,dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)
    
    res = bin(whole).lstrip("0b") + "."
    for x in range(places):
        whole,dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res +=whole
        
    return res

def decimal_converter(num):
    while num > 1:
        num /=10
    return num
    
    
param1 = {'gear-2-ratio': np.array([69]),
              'gear-3-ratio': np.array([69]),
              'gear-4-ratio': np.array([69]),
              'gear-5-ratio': np.array([1.5]),
              'gear-6-ratio': np.array([1.0]),
              'rear-differential-ratio': np.array([4.5]),
              'rear-spoiler-angle': np.array([14.0]),
              'front-spoiler-angle': np.array([6.0])}
param2 = {'gear-2-ratio': np.array([2.5]),
              'gear-3-ratio': np.array([1.5]),
              'gear-4-ratio': np.array([1.5]),
              'gear-5-ratio': np.array([1.5]),
              'gear-6-ratio': np.array([1.0]),
              'rear-differential-ratio': np.array([4.5]),
              'rear-spoiler-angle': np.array([69]),
              'front-spoiler-angle': np.array([69.0])}

kid1,kid2 = sexy_time3(param1,param2,8)
print(kid2)
#float_to_bin(parameters)