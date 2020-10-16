#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 08:58:43 2020

@author: user
"""

import numpy as np
from nipype.utils.filemanip import loadpkl

import tensorflow as tf
from keras.models import Sequential, load_model
from keras import layers
from keras.optimizers import Adam, SGD

from keras import backend as K
from keras.utils.generic_utils import get_custom_objects

#########################################
# Create neural network
#########################################
def create_nn_model(size_in, size_out):
        
    model = Sequential()
    model.add(layers.Dense(units= size_in*1, activation='sigmoid', input_shape= (size_in,)))
    model.add(layers.Dense(units= size_out, activation='sigmoid'))
    
    return model


def bell(x_in):
    [a, b, c] = [0, 1, 1]
    return 1/(1+((x_in**2-a)/c)**(2*b))
#
#
def create_anfis_model(size_in, size_out):
        
    model = Sequential()
    model.add(layers.Input(shape=(size_in,)))
    model.add(layers.Activation('sigmoid'))
    model.add(layers.multiply())
    
    return model


def vision(capteur):
    dg = np.mean(capteur[0:8])/100
    dc = capteur[9]/100
    dd = np.mean(capteur[10:18])/100
    
    vis = np.array([[dg, dc, dd]], dtype=np.float32)
    
    return vis


#########################################
# Creating training data
#########################################
def load_dataset(file, valid_per):
    
    # open a file, where you stored the pickled data
    data_loaded = loadpkl(file)
    
    size = len(data_loaded) 
    
    # inputs (observations)
    angle_data = np.empty((size, 1), dtype=np.float32)
    gear_data = np.empty((size, 1), dtype=np.float32)
    rpm_data = np.empty((size, 1), dtype=np.float32)
    speed_data = np.empty((size, 2), dtype=np.float32)
    track_data = np.empty((size, 19), dtype=np.float32)
    trackpos_data = np.empty((size, 1), dtype=np.float32)
    
    # outputs (action)
    accel_target = np.empty((size, 1), dtype=np.float32)
    brake_target = np.empty((size, 1), dtype=np.float32)
    gear_target = np.empty((size, 1), dtype=np.float32)
    steer_target = np.empty((size, 1), dtype=np.float32)
    
    for i in range(size):
        angle_data[i, 0] = data_loaded[i]['angle']
        gear_data[i, 0] = data_loaded[i]['gear'] * 0.1
        rpm_data[i, 0] = data_loaded[i]['rpm']
        speed_data[i, :] = data_loaded[i]['speed']
        track_data[i, :] = data_loaded[i]['track']
        trackpos_data[i, 0] = data_loaded[i]['trackPos']
    
        accel_target[i, 0] = data_loaded[i]['accelCmd']
        brake_target[i, 0] = data_loaded[i]['brakeCmd']
        gear_target[i, 0] = data_loaded[i]['gearCmd'] * 0.1
        steer_target[i, 0] = data_loaded[i]['steerCmd']*0.5 + 0.5
        
    data_temp = np.concatenate((angle_data, gear_data, speed_data, track_data, trackpos_data), axis=1)  
    target_temp = np.concatenate((accel_target, brake_target, gear_target, steer_target), axis=1)
    
    set_number, size_in = data_temp.shape
    _, size_out = target_temp.shape
    
    valid_set_size = round(set_number*valid_per)
    set_number = set_number - valid_set_size
    
    
    valid_data = data_temp[0:valid_set_size, :]
    valid_target = target_temp[0:valid_set_size, :]
    
    data = data_temp[valid_set_size:, :]
    target = target_temp[valid_set_size:, :]
    

    #data = np.concatenate((speed_data, track_data, trackpos_data), axis=1)
    #target = np.concatenate((accel_target, brake_target, steer_target), axis=1)
    
    return data, target, valid_data, valid_target, size_in, size_out













