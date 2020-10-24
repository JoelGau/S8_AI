# Copyright (c) 2018, Simon Brodeur
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  - Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE, DATA,
# OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author: Simon Brodeur <simon.brodeur@usherbrooke.ca>
# Université de Sherbrooke, APP3 S8GIA, A2018

import os
import sys
import time
import numpy as np
import logging
import GA_module as ga
import copy as cp

import matplotlib.pyplot as plt


sys.path.append('../..')
from torcs.optim.core import TorcsOptimizationEnv, TorcsException

CDIR = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)


################################
# Define helper functions here
################################

def main(nb_epoch, population):
    list_epoch =  []
    list_fitness = []
    list_FitMoy = []
    temp_list_fitness = []
    Best = ga.Chromosome()
    Best.fitnessEconomique = 9999
    Best.fitnessSport = 0
    try:
        maxEvaluationTime = 100.0  # sec
        with TorcsOptimizationEnv(maxEvaluationTime) as env:
            
            Mypop = ga.Population()
            Mypop.generatePopulation(population)
            # Loop a few times for demonstration purpose
            for i in range(0,nb_epoch):
                print("Epoch : ", i, "      ")
                for individu in Mypop.Individus:
                     # Simulate the result of each individual
                    individu.observation, _, _, _ = env.step(individu.to_param())
                    if not individu.observation:
                        print("Torcs failed")                                   
                    # Calculate fitness
                    individu.fitnessSpo(maxEvaluationTime)
                # List individual in priority of fitness value
                Mypop.sortIndividualSport()
                # Save Fitness for futher evaluation
                for individu in Mypop.Individus:
                    temp_list_fitness.append(individu.fitnessSport)
                # Save the mean fitness of the population
                list_FitMoy.append(np.mean(temp_list_fitness))
                # Save all the fitness in the population
                list_fitness.extend(temp_list_fitness)
                temp_list_fitness.clear()
                # Save the best candidate
                print(Best.fitnessSport)
                if (Best.fitnessSport < Mypop.Individus[0].fitnessSport):
                    print("New Best!")
                    Best = cp.copy(Mypop.Individus[0])
                Mypop.nextGeneration_Starbuck()

    except TorcsException as e:
        logger.error('Error occured communicating with TORCS server: ' + str(e))

    except KeyboardInterrupt:
        pass
    

    logger.info('All done.')
    logger.info(list_epoch)
    
    return Best, list_FitMoy, list_fitness

def AffichageFitnessEco(list_fitness, population, nb_epoch):
    # Evaluate ecofitness between generations
    plt.figure()
    plt.plot(list_fitness)
    plt.title("Fitness des différents individus")
    plt.xlabel('Individus')
    plt.ylabel('Fitness (Smaller is better)')
    plt.ylim(top=0.0007)
    plt.xlim(left=0, right=population*nb_epoch-1)
    for i in range (0,nb_epoch-1):
        plt.vlines((i+1)*population-1,0,0.0007,linestyle = 'dashed')
    plt.show()
    
def AffichageFitnessSpo(list_fitness, population, nb_epoch):
    # Evaluate ecofitness between generations
    plt.figure()
    plt.plot(list_fitness)
    plt.title("Fitness des différents individus")
    plt.xlabel('Individus')
    plt.ylabel('Fitness (Bigger is better)')
    plt.xlim(left=0, right=population*nb_epoch-1)
    for i in range (0,nb_epoch-1):
        plt.vlines((i+1)*population-1,0,1000,linestyle = 'dashed')
    plt.show()
    
def AffichageFitMoyEco(list_FitMoy, nb_epoch):
    plt.figure()
    plt.plot(list_FitMoy)
    plt.title("Fitness moyen des populations")
    plt.xlabel('Générations')
    plt.ylabel('Fitness (Smaller is better)')
    plt.show()

def AffichageFitMoySpo(list_FitMoy, nb_epoch):
    plt.figure()
    plt.plot(list_FitMoy)
    plt.title("Fitness moyen des populations")
    plt.xlabel('Générations')
    plt.ylabel('Fitness (Bigger is better)')
    plt.show()

def test():

    try:
        maxEvaluationTime = 60.0  # sec
        with TorcsOptimizationEnv(maxEvaluationTime) as env:
            myChrom = ga.Chromosome()
            myChrom.aar = 250
            myChrom.aav = 670
            myChrom.dgr = 31
            myChrom.gr2 = 20
            myChrom.gr3 = 24
            myChrom.gr4 = 50
            myChrom.gr5 = 42
            myChrom.gr6 = 15
            for i in range(5):
                 # Simulate the result of each individual
                myChrom.observation, _, _, _ = env.step(myChrom.to_param())                                         
                # Calculate fitness
                myChrom.fitnessEco()
                print(myChrom.fitnessEconomique)

    except TorcsException as e:
        logger.error('Error occured communicating with TORCS server: ' + str(e))

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    nb_epoch = 10
    population = 50
    logging.basicConfig(level=logging.INFO)
    best, moy, every = main(nb_epoch, population)
    AffichageFitMoySpo(moy, nb_epoch)
    AffichageFitnessSpo(every, population, nb_epoch)
    #test()
    




    
#class Population:
#    def __init__(self,parameters):
        