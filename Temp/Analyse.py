#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:24:50 2022

@author: frichard
"""
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, AveragePooling2D, Dense
from tensorflow.keras.layers import Lambda, Flatten
from tensorflow.math import log, pow
from tensorflow.random import normal
from tensorflow.keras.callbacks import ModelCheckpoint, TerminateOnNaN
from BatchGenerator import Custom_Generator
from Protocol import protocol


def Quadratic(x):
    return(pow(x, 2))


def Log(x):
    return(log(x))


# Parameter for the definition of the CNN
nlayers = 4  # number of convolutional layers
filtsize = 3  # size of convolution kernels.

# Parameter for the learning of the CNN
# Set the learning and testing parameters.
# Number of examples used for learning the CNN.
N00 = 0
N01 = 4999
# Number of examples used for validation while learning the CNN.
N10 = 5000
N11 = 7499
# Number of examples used for testing data.
N20 = 7500
N21 = 9999
# Number of epochs used for learning the DNN.
n_epochs = 200
# Batch size.
batch_size = 50
# Loss function.
loss = "Mean_Squared_Error"
# Learning rate
lr = 10e-2
# Features to be estimated.
f0 = 0

rep_root = "/home/frederic/Database/PyAFBF-textures/"
rep_data = rep_root + "SimulationSet_001/"
output_file = "CNNModels/" + "CNNModel_001"

# Set the database.
simu = protocol(rep_data)
simu.LoadExample(0)
training_set = Custom_Generator(simu, N00, N01, batch_size, f0)
validation_set = Custom_Generator(simu, N10, N11, batch_size, f0)
test_set = Custom_Generator(simu, N20, N21, batch_size, f0)


# Set the CNN model
model = Sequential()
nchannels = 1
nfilters = 2
N = simu.N
for j in range(nlayers):
    model.add(
        Conv2D(
            nfilters,
            filtsize,
            strides=1,
            # groups=nchannels,
            activation=None,
            use_bias=False,
            name="conv" + str(j),
        )
    )
    nchannels = nfilters
    nfilters = nfilters * 2

N = N - nlayers * (filtsize - 1)
model.add(Lambda(Quadratic, name='quadratic'))
model.add(
    AveragePooling2D(
        pool_size=(N, N),
        strides=None,
        name="variations"
    ))
model.add(Lambda(Log, name='log'))
model.add(Dense(1, name='regression'))
model.add(Flatten())

z = model(normal([1, simu.N, simu.N, 1]))
model.summary()

model.compile(loss="MSE", optimizer="Adam")


# Call back : for saving the model.
checkpoint = ModelCheckpoint(
    filepath='model-cnn',
    save_weights_only=True,
    monitor="val_loss",
    verbose=1,
    save_best_only=True,
    mode="min",
    save_freq="epoch",
)

# To stop iterations in the cas of divergence.
term_nan = TerminateOnNaN()

history = model.fit(
    x=training_set,
    steps_per_epoch=len(training_set),
    epochs=n_epochs,
    verbose=1,
    callbacks=[checkpoint, term_nan],
    validation_data=validation_set,
    workers=1,
    use_multiprocessing=False,
)

model.evaluate(test_set)
