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
    def __init__(self, gr2, gr3, gr4, gr5, gr6, dgr, aav, aar):
        self.gr2 = gr2
        self.gr3 = gr3
        self.gr4 = gr4
        self.gr5 = gr5
        self.gr6 = gr6
        self.dgr = dgr
        self.aav = aav
        self.aar = aar
        self.observation = []
        self.fitnessEconomique = 0
        self.fitnessSport = 0
        
    def __init__(self):
        self.gr2 = rd.randint(1,50)
        self.gr3 = rd.randint(1,50)
        self.gr4 = rd.randint(1,50)
        self.gr5 = rd.randint(1,50)
        self.gr6 = rd.randint(1,50)
        self.dgr = rd.randint(10,100)
        self.aav = rd.randint(0,900)
        self.aar = rd.randint(0,900)
        self.observation = []
        self.fitnessEconomique = 0
        self.fitnessSport = 0
        
    def to_param(self):
        parameters =   {'gear-2-ratio': np.array([float(self.gr2)/10]), 
                        'gear-3-ratio': np.array([float(self.gr3)/10]), 
                        'gear-4-ratio': np.array([float(self.gr4)/10]), 
                        'gear-5-ratio': np.array([float(self.gr5)/10]), 
                        'gear-6-ratio': np.array([float(self.gr6)/10]), 
                        'rear-differential-ratio': np.array([float(self.dgr)/10]), 
                        'rear-spoiler-angle': np.array([float(self.aav)/10]), 
                        'front-spoiler-angle': np.array([float(self.aar)/10])}
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
    
    def generatePopulation(self,length):
        for i in range(length):
            ind = Chromosome()
            self.Individus.append(ind)
            
    def nextGeneration(self):
        for i in range(0, len(self.Individus), 2):
            st.sexyTime_5050(self.Individus[i], self.Individus[i+1])
        
    def nextGeneration_Survivors(self):
        keep = round(len(self.Individus)/5)
        Bests = self.Individus[0:keep]
        self.Individus = self.Individus[:len(self.Individus)-keep]
        for i in range(0, len(self.Individus), 2):
            st.sexyTime_minmax(self.Individus[i], self.Individus[i+1])
        self.Individus + Bests
    
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

def binariseChromosome(chromosome):
    gr2 = bin(int(chromosome.gr2*10))
    gr3 = bin(int(chromosome.gr3*10))
    gr4 = bin(int(chromosome.gr4*10))
    gr5 = bin(int(chromosome.gr5*10))
    gr6 = bin(int(chromosome.gr6*10))
    dgr = bin(int(chromosome.dgr*10))
    aav = bin(int(chromosome.aav*10))
    aar = bin(int(chromosome.aar*10))
    return gr2, gr3, gr4, gr5, gr6, dgr, aav, aar

def unbinariseChromosome(gr2, gr3, gr4, gr5, gr6, dgr, aav, aar): 
    gr2 = float(gr2)/10
    gr3 = float(gr3)/10
    gr4 = float(gr4)/10
    gr5 = float(gr5)/10
    gr6 = float(gr6)/10
    dgr = float(dgr)/10
    aav = float(aav)/10
    aar = float(aar)/10
    return Chromosome(gr2,gr3,gr4,gr5,gr6,dgr,aav,aar)
    

#Test
    
#mychro = Chromosome()