import numpy as np
import random as rd
import sexy_time as st
import copy as cp

class Chromosome:             
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
        c1 = 3
        c2 = 7
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
        
    def nextGeneration_Starbuck(self):
        # Gets the bests candidate
        Best = cp.copy(self.Individus[0])
        for i in range(0, len(self.Individus), 2):
            # In case it is unheaven
            try:
                self.Individus[i] = Best
                st.sexyTime_Mutation50(self.Individus[i], self.Individus[i+1])
            except:
                pass
        # Add the starbuck to the population
        #self.Individus = self.Individus.append(Best)
    
    def nextGeneration_Survivors(self, qty):
        # Gets the bests candidate
        Bests = self.Individus[0:qty]
        # Eliminates worts candidates
        self.Individus = self.Individus[:len(self.Individus)-qty]
        for i in range(0, len(self.Individus), 2):
            # In case it is unheaven
            try:
                st.sexyTime_Mutation50(self.Individus[i], self.Individus[i+1])
            except:
                pass
        # Add the bests parents to the population
        self.Individus = self.Individus + Bests
        
    def nextGeneration_Mutation(self, qty):
        # Gets the bests candidate
        Bests = self.Individus[0:qty]
        # Eliminates worts candidates
        self.Individus = self.Individus[:len(self.Individus)-qty]
        for i in range(0, len(self.Individus), 2):
            # Breeding
            if(rd.randint(0,9) > 2):
                try:
                    st.sexyTime_Mutation50(self.Individus[i], self.Individus[i+1])
                except:
                    pass
            # Mutation
            else:
                try:
                    # New random chromosomes
                    self.Individus[i].__init__()
                    self.Individus[i+1].__init__()
                except:
                    self.Individus[i].__init__()
        # Add the bests parents to the population
        self.Individus = self.Individus + Bests
    
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
