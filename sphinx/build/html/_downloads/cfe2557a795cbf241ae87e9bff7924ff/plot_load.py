#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================
Load and manage an existing database
====================================

.. codeauthor:: Frédéric Richard <frederic.richard_at_univ-amu.fr>
"""
# Import a simulation protocol.
from afbfdb import protocol


# directory to save examples.
root_dir = "../data/"
data_dir = root_dir + "SimulationSet_001/"

# Load the protocol.
simu = protocol(data_dir)
# Show an example.
simu.ShowExample(5)
