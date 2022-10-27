#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================
Build a database using a predefined protocol
============================================

.. codeauthor:: Frédéric Richard <frederic.richard_at_univ-amu.fr>
"""

from afbfdb.Protocol import Protocol_001

# directory to save examples.
root_dir = "../data/"
data_dir = root_dir + "TestSet/"

N = 512  # image size
last_example = 9  # index of the last example.
_save = True  # true if examples are to be saved.
_display = False  # true if examples are to be displayed.

# Set the protocol.
simu = Protocol_001(data_dir, N=N)
# Simulate fields.
simu.SimulateFields(_save=_save, _display=_display,
                    expe_start=0, expe_end=last_example)
# Show an example.
simu.ShowExample(2)
