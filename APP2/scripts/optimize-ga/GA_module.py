#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 10:20:19 2020

@author: user
"""
import numpy as np
import random as rd
import sexy_time as st

class Chromosome:      
    def __init__(self):
        self.gr2 = float(rd.randint(1,50))/10
        self.gr3 = float(rd.randint(1,50))/10
        self.gr4 = float(rd.randint(1,50))/10
        self.gr5 = float(rd.randint(1,50))/10
        self.gr6 = float(rd.randint(1,50))/10
        self.dgr = float(rd.randint(10,100))/10
        self.aav = float(rd.randint(0,900))/10
        self.aar = float(rd.randint(0,900))/10
        self.observation = []
        self.fitnessEconomique = 0
        self.fitnessSport = 0
        
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
    
    def fitnessEco(self):
        self.fitnessEconomique = self.observation['fuelUsed'][0]/self.observation['distRaced'][0]
        
    def fitnessSpo(self, time):
        acceleration = self.observation['distRaced'][0]/time/time
        c1 = 1
        c2 = 1
        self.fitnessSport = c1 * self.observation['topspeed'][0] + c2 * acceleration
        

class Population:
    def __init__(self):
        self.Individus = []
    
    def calcultateFitness(self):
        pass
    
    def generatePopulation(self,length):
        for i in range(length):
            ind = Chromosome()
            self.Individus.append(ind)
        
    def nextGeneration(self):
        for i in range(0, len(self.Individus), 2):
            st.sexy_time2(self.Individus[i], self.Individus[i+1])
            

    def sortIndividualSport(self):
        self.Individus.sort(key = takefitnessSport, reverse = True)
        
    def sortIndividualEconomique(self):
        self.Individus.sort(key = takefitnessEco)
        
# keys to spo
def takefitnessSport(elem):
    return elem.fitnessSport

# keys to eco
def takefitnessEco(elem):
    return elem.fitnessEconomique
