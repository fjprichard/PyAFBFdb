#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================
Export the data.
================

.. codeauthor:: Frédéric Richard <frederic.richard_at_univ-amu.fr>
"""
# Import a simulation protocol.
from afbfdb import protocol
from matplotlib import pyplot as plt
from numpy import zeros, savetxt, uint16, amin, amax
from imageio.v2 import imsave
import os

# directory to save examples.
home_dir = "../data/"
data_dir = home_dir + "SimulationSet_001/"
data_out = home_dir + "SimulationSet_001-export/"

# Load the protocol.
simu = protocol(data_dir)
n = simu.nbexpe
simu.ShowExample(7)
# Export the data in a numpy array format.
images, features = simu.ExportData(0, n-1)
# Show an image and its features.
plt.figure()
plt.imshow(images[7, :, :], cmap="gray")
plt.show()
print("Exported features:")
print(features[7, :])

if os.path.isdir(data_out) is False:
    os.mkdir(data_out)
# Export features in csv format.
header = 'Hurst index, argmin set length, argmin set center, Hmax'
savetxt(data_out + 'features.csv', features, delimiter=',', header=header)


# Export images in png format.
m = images.shape[1:]
glmax = 2**16 - 1
image = zeros(m, dtype=uint16)
for expe in range(n):
    ide = simu.SetExampleNumberStr(expe)
    # Conversion of the image into uint16 by normalization.
    immin = amin(images[expe, :, :])
    immax = amax(images[expe, :, :])
    imrange = immax - immin
    image[:, :] = (images[expe, :, :] - immin) / imrange * glmax
    # Save the image.
    imsave(data_out + "image-" + ide + ".png", image)
