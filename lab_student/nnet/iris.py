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
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author: Simon Brodeur <simon.brodeur@usherbrooke.ca>
# Université de Sherbrooke, APP3 S8GIA, A2018
import matplotlib.pyplot as plt
import numpy as np
import scipy.io

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import SGD

###############################################
# Define helper functions here
###############################################


###############################################
# Define code logic here
###############################################

def main():

    # Load iris data set from file
    # Attributes are: petal length, petal width, sepal length, sepal width
    # TODO: Analyze the input data
    S = scipy.io.loadmat('iris.mat')
    data = np.array(S['data'], dtype=np.float32)
    target = np.array(S['target'], dtype=np.float32)

   # np.histogram(data,bins=10,range=None, normed = 1, weights=None, desity=None)

    #plt.plot(data[:,0],data[:,1], data[:,3])
    #plt.show()
    # TODO : Apply any relevant transformation to the data
    # (e.g. filteringdu, normalization, dimensionality rection)
    for i in range(0,3):
        data[:,i] = data[:,i]/data[:,i].max() # Normalize
    
    # Create neural network
    # TODO : Tune the number and size of hidden layers
    model = Sequential()
    model.add(Dense(units=16, activation='sigmoid',
                    input_shape=(data.shape[-1],)))  # input shape = 4
    model.add(Dense(units=target.shape[-1], activation='tanh')) #output shape = 3
    print(model.summary())

    # Define training parameters
    # TODO : Tune the training parameters
    model.compile(optimizer=SGD(lr=0.5, momentum=0.9),
                  loss='mse')

    # Perform training
    # TODO : Tune the maximum number of iterations
    model.fit(data, target, batch_size=len(data),
              epochs=1000, shuffle=True, verbose=1)

    # Save trained model to disk
    model.save('iris.h5')

    # Test model (loading from disk)
    model = load_model('iris.h5')
    targetPred = model.predict(data)

    # Print the number of classification errors from the training data
    nbErrors = np.sum(np.argmax(targetPred, axis=-1) != np.argmax(target, axis=-1))
    accuracy = (len(data) - nbErrors) / len(data)
    print('Classification accuracy: %0.3f' % (accuracy))


if __name__ == "__main__":
    main()
