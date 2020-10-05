#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 10:20:19 2020

@author: user
"""
import numpy as np

class Chromosomes:
    def __init__(self):
        self.gr2 = 1.7
        self.gr3 = 1.6
        self.gr4 = 2.8
        self.gr5 = 1.1
        self.gr6 = 1.0
        self.dgr = 8.6
        self.aav = 45
        self.aar = 45
        self.observation = []
        
    def to_param(self):
        parameters =   {'gear-2-ratio': np.array([self.gr2]), 
                        'gear-3-ratio': np.array([self.gr3]), 
                        'gear-4-ratio': np.array([self.gr4]), 
                        'gear-5-ratio': np.array([self.gr5]), 
                        'gear-6-ratio': np.array([self.gr6]), 
                        'rear-differential-ratio': np.array([self.dgr]), 
                        'rear-spoiler-angle': np.array([self.aav]), 
                        'front-spoiler-angle': np.array([self.aar])}
        return parameters
