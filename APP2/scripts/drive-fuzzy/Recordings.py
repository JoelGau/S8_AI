#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:11:39 2020

@author: user
"""

import pickle

filename = "recordings/track-alpine-1.pklz"

file = open(filename, "rb")
new_dict = pickle.load(file)

file.close()