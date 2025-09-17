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

nb_examples = 9  # Number of examples.
_save = True  # true if examples are to be saved.
_display = False  # true if examples are to be displayed.

# Set the protocol.
simu = protocol(data_dir)
# Simulate fields.
simu.SimulateFields(expe_end=nb_examples, _save=_save, _display=_display)
# Show an example.
simu.ShowExample(2)
