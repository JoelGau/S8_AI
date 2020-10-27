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

from comet_ml import Experiment
import os
import sys
import time
import logging
import numpy as np
import math
from keras.optimizers import SGD


import nn_module as nn



sys.path.append('../..')
from torcs.control.core import TorcsControlEnv, TorcsException, EpisodeRecorder

CDIR = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)



train = True



experiment = Experiment(api_key="oXuZfAKkB3UrV8H78EqqBAkzL",
                    project_name="app2", workspace="bertsam", log_code=True)

nb_epoch = 20000
learning_rate = 0.5
valid_split = 0.1

save_name = str('car_ride_itt_5_ep=' + str(nb_epoch) + '_HlSize=24.h5')

if train:

    
    # Controle rules data set
    dataset = nn.build_dataset('../drive-simple/recordings/')
    data, target, size_in, size_out = nn.load_dataset(dataset)
    #data, target, size_in, size_out = nn.load_dataset('../drive-bot/recordings/track.pklz')
    
    model = nn.create_nn_model(size_in, size_out)
    
    # Define training parameters
    model.compile(optimizer = SGD(lr = learning_rate), loss='mse')
    

    # log your  parameters to Comet.ml!
    params = {"learning_rate": learning_rate,
              "batch_size": len(data),
              "nb_epoch": nb_epoch
              }
    
    experiment.log_parameters(params)
    
    print(model.summary())
    
    print('Training...')

    # Perform training
    #model.fit(data, target, batch_size=len(data), epochs=nb_epoch, shuffle=True, verbose=1)
    model.fit(data, target,
                batch_size=len(data),
                epochs = nb_epoch,
                shuffle=True,
                verbose=0,
                validation_split = valid_split)
    
    
    model.save(save_name)

else:
    model = load_model("car_ride_epoch_V3=20000_HlSize=24.h5")
    from ann_visualizer.visualize import ann_viz
    ann_viz(model, title="My first neural network")
        
    _, size_in = model.input_shape
    _, size_out = model.output_shape
    


def main():

    recordingsPath = os.path.join(CDIR, 'recordings')
    if not os.path.exists(recordingsPath):
        os.makedirs(recordingsPath)

    try:
        with TorcsControlEnv(render=False) as env:

            nbTracks = len(TorcsControlEnv.availableTracks)
            nbSuccessfulEpisodes = 0
            for episode in range(nbTracks):
                logger.info('Episode no.%d (out of %d)' % (episode + 1, nbTracks))
                startTime = time.time()

                observation = env.reset()
                trackName = env.getTrackName()

                nbStepsShowStats = 1000
                curNbSteps = 0
                done = False
                with EpisodeRecorder(os.path.join(recordingsPath, 'track-%s.pklz' % (trackName))) as recorder:
                    while not done:
                        # TODO: Select the next action based on the observation
                        action = env.action_space.sample()
                        recorder.save(observation, action)
      
                        #rint(observation)
                        
                        angle = observation["angle"]
                        gear = observation["gear"]
                        rpm = observation["rpm"]
                        speed = observation["speed"]
                        track = observation["track"]
                        trackpos = observation["trackPos"]
                        

                        proch_action = np.empty((1, size_in))
                      
                        
                        proch_action[0, :] = np.concatenate((angle, gear, speed, track, trackpos), axis=0)
                        
                        
                        pred = model.predict(proch_action)
                        
                        action['accel'][0] = pred[0, 0]
                        action['brake'][0] = pred[0, 1]
                        action['gear'][0] = math.ceil(pred[0, 2]*10)
                        action['steer'][0] = (pred[0, 3]-0.5)*2
                        
#                        while action['gear'][0] > 6:
#                            action['gear'][0] = action['gear'][0] - 1
                        
                  
                        
                       # Execute the action
                        observation, reward, done, _ = env.step(action)
                        curNbSteps += 1
  
    
                        if observation and curNbSteps % nbStepsShowStats == 0:
                            curLapTime = observation['curLapTime'][0]
                            distRaced = observation['distRaced'][0]
                            logger.info('Current lap time = %4.1f sec (distance raced = %0.1f m)' % (curLapTime, distRaced))
    
                        if done:
                            if reward > 0.0:
                                logger.info('Episode was successful.')
                                nbSuccessfulEpisodes += 1
                            else:
                                logger.info('Episode was a failure.')
    
                            elapsedTime = time.time() - startTime
                            logger.info('Episode completed in %0.1f sec (computation time).' % (elapsedTime))

            logger.info('-----------------------------------------------------------')
            logger.info('Total number of successful tracks: %d (out of %d)' % (nbSuccessfulEpisodes, nbTracks))
            logger.info('-----------------------------------------------------------')

    except TorcsException as e:
        logger.error('Error occured communicating with TORCS server: ' + str(e))

    except KeyboardInterrupt:
        pass

    logger.info('All done.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
