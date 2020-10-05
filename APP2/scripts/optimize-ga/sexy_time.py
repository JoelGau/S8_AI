#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:24:04 2020

@author: Laurent Colas
"""

import numpy as np


def sexy_time(p1,p2):
    kid1 = {'gear-2-ratio': p1['gear-2-ratio'], 
            'gear-3-ratio': p2['gear-3-ratio'], 
            'gear-4-ratio': p1['gear-4-ratio'], 
            'gear-5-ratio': p2['gear-5-ratio'], 
            'gear-6-ratio': p1['gear-6-ratio'], 
            'rear-differential-ratio': p2['rear-differential-ratio'], 
            'rear-spoiler-angle': p1['rear-spoiler-angle'], 
            'front-spoiler-angle': p2['front-spoiler-angle']}
    
    kid2 = {'gear-2-ratio': p2['gear-2-ratio'], 
            'gear-3-ratio': p1['gear-3-ratio'], 
            'gear-4-ratio': p2['gear-4-ratio'], 
            'gear-5-ratio': p1['gear-5-ratio'], 
            'gear-6-ratio': p2['gear-6-ratio'], 
            'rear-differential-ratio': p1['rear-differential-ratio'], 
            'rear-spoiler-angle': p2['rear-spoiler-angle'], 
            'front-spoiler-angle': p1['front-spoiler-angle']}
    
    return (kid1, kid2)
    

def sexy_time2(p1,p2):
    gear2ratio = find_big(p1['gear-2-ratio'][0], p2['gear-2-ratio'][0])
    gear3ratio = find_big(p1['gear-3-ratio'][0], p2['gear-3-ratio'][0])
    gear4ratio = find_big(p1['gear-4-ratio'][0], p2['gear-4-ratio'][0])
    gear5ratio = find_big(p1['gear-5-ratio'][0], p2['gear-5-ratio'][0])
    gear6ratio = find_big(p1['gear-6-ratio'][0], p2['gear-6-ratio'][0])
    reardifferentialratio = find_big(p1['rear-differential-ratio'][0], p2['rear-differential-ratio'][0])
    rearspoilerangle = find_big(p1['rear-spoiler-angle'][0], p2['rear-spoiler-angle'][0])
    frontspoilerangle = find_big(p1['front-spoiler-angle'][0], p2['front-spoiler-angle'][0])
    kid1 = {'gear-2-ratio': np.array([gear2ratio]),
            'gear-3-ratio': np.array([gear3ratio]), 
            'gear-4-ratio': np.array([gear4ratio]), 
            'gear-5-ratio': np.array([gear5ratio]), 
            'gear-6-ratio': np.array([gear6ratio]), 
            'rear-differential-ratio': np.array([reardifferentialratio]), 
            'rear-spoiler-angle': np.array([rearspoilerangle]), 
            'front-spoiler-angle': np.array([frontspoilerangle])}
    
    gear2ratio = find_small(p1['gear-2-ratio'][0], p2['gear-2-ratio'][0])
    gear3ratio = find_small(p1['gear-3-ratio'][0], p2['gear-3-ratio'][0])
    gear4ratio = find_small(p1['gear-4-ratio'][0], p2['gear-4-ratio'][0])
    gear5ratio = find_small(p1['gear-5-ratio'][0], p2['gear-5-ratio'][0])
    gear6ratio = find_small(p1['gear-6-ratio'][0], p2['gear-6-ratio'][0])
    reardifferentialratio = find_small(p1['rear-differential-ratio'][0], p2['rear-differential-ratio'][0])
    rearspoilerangle = find_small(p1['rear-spoiler-angle'][0], p2['rear-spoiler-angle'][0])
    frontspoilerangle = find_small(p1['front-spoiler-angle'][0], p2['front-spoiler-angle'][0])
    kid2 = {'gear-2-ratio': np.array([gear2ratio]),
            'gear-3-ratio': np.array([gear3ratio]), 
            'gear-4-ratio': np.array([gear4ratio]), 
            'gear-5-ratio': np.array([gear5ratio]), 
            'gear-6-ratio': np.array([gear6ratio]), 
            'rear-differential-ratio': np.array([reardifferentialratio]), 
            'rear-spoiler-angle': np.array([rearspoilerangle]), 
            'front-spoiler-angle': np.array([frontspoilerangle])}
    
    return (kid1,kid2)
    

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