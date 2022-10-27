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

# directory to save examples.
root_dir = "../data/"
data_dir = root_dir + "SimulationSet_001/"

# Load the protocol.
simu = protocol(data_dir)
simu.ShowExample(7)
# Export the data
images, features = simu.ExportData(0, 9)
# Show an image and features.
plt.figure()
plt.imshow(images[7, :, :], cmap="gray")
plt.show()
print("Exported features:")
print(features[7, :])
