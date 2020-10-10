#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 08:58:43 2020

@author: user
"""

import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from keras import backend as K
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import SGD


# creating training data
def build_dataset():
    rules = [1.0,1.0,1.0,1.0,0.5,0.5,1.0,1.0,0.6,0.7,1.0,1.0,0.5,0.6,0.3,1.0,0.5,1.0,0.3,0.4,0.5,1.0,0.5,0.7,0.5,0.0,0.0,0.0,0.2,0.2,0.5,0.5,0.5,0.5,0.4,0.0,1.0,1.0,0.4,0.9,1.0,1.0,0.0,0.4,0.1,1.0,0.0,1.0,0.2,0.2,0.0,1.0,0.0,1.0,0.5,0.0,0.0,1.0,0.3,0.8,1.0,0.0,0.0,0.3,0.2,0.3,0.4,0.1,0.5,0.3,0.1,0.4,0.3,0.5,0.7,0.0,0.1,0.2,0.3,0.9,0.2,0.1,0.0,0.3,0.1,0.0,0.3,0.6,0.5,0.8,0.6,0.3,0.0,0.5,0.2,0.2,0.3,0.4,0.5,0.9,0.4,0.3,0.2,0.4,0.1]
    data = np.empty((int(len(rules)/5), 3), dtype=np.float32) 
    target = np.empty((int(len(rules)/5), 2), dtype=np.float32) 
    in_rule_frame = np.empty((5)) 
    
    for i in range(0, len(rules), 5): 
        in_rule_frame[:] = rules[i:i+5] 
        data[int(i/5), :] = in_rule_frame[0:3] 
        target[int(i/5), :] = in_rule_frame[3:5]
    
    return data, target

def vision(capteur):
    dg = np.mean(capteur[0:8])/100
    dc = capteur[9]/100
    dd = np.mean(capteur[10:18])/100
    
    vis = np.array([[dg, dc, dd]], dtype=np.float32)
    
    return vis














