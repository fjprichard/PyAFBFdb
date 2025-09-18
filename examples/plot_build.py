#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================
Build a database using a predefined protocol
============================================

.. codeauthor:: Frédéric Richard <frederic.richard_at_univ-amu.fr>
"""
from afbfdb.Protocol import protocol
# directory to save examples.
home_dir = "../data/"
data_dir = home_dir + "TestSet/"

nb_examples = 10  # Number of examples.

# Set the protocol.
simu = protocol(data_dir)
# Simulate fields.
simu.CreateFields(expe_end=nb_examples)
# Show an example.
simu.ShowExample(2)
