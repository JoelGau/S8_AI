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

import matplotlib.pyplot as plt


sys.path.append('../..')
from torcs.optim.core import TorcsOptimizationEnv, TorcsException

CDIR = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)

list_epoch =  []
list_fitness = []

nb_epoch = 10
population = 40
################################
# Define helper functions here
################################

def main():

    try:
        maxEvaluationTime = 50.0  # sec
        with TorcsOptimizationEnv(maxEvaluationTime) as env:
            
            Mypop = ga.Population()
            Mypop.generatePopulation(population)
            # Loop a few times for demonstration purpose
            for i in range(0,nb_epoch):
                list_epoch = []
                print("Epoch : ", i, "      ")
                for individu in Mypop.Individus:
                     # Simulate the result of each individual
                    individu.observation, _, _, _ = env.step(individu.to_param())
                    list_epoch.append(individu.observation)
                                         
                    # Calculate fitness
                    individu.fitnessEco()
                # List individual in priority of fitness value
                Mypop.sortIndividualEconomique()
                # Save Fitness for futher evaluation
                for individu in Mypop.Individus:
                    list_fitness.append(individu.fitnessEconomique)
                Mypop.nextGeneration()
                
                logger.info(list_epoch)

    except TorcsException as e:
        logger.error('Error occured communicating with TORCS server: ' + str(e))

    except KeyboardInterrupt:
        pass
    

    logger.info('All done.')
    logger.info(list_epoch)
    
    # Evaluate fitness between generations
    plt.plot(list_fitness)
    plt.title("Fitness des différents individus")
    plt.xlabel('Individus')
    plt.ylabel('Fitness (Smaller is better)')
    plt.ylim(top=0.0007)
    plt.xlim(left=0, right=population*nb_epoch-1)
    for i in range (0,nb_epoch-1):
        plt.vlines((i+1)*population-1,0,0.0007,linestyle = 'dashed')
    plt.show()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()




    
#class Population:
#    def __init__(self,parameters):
        