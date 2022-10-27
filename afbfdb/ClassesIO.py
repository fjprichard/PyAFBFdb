#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tools for I/O of class objects of the PyAFBF package.
"""

from afbf.utilities import floor_divide, pickle
from afbf import tbfield, perfunction, sdata


def SaveTBfield(model, filename):
    """Load the tbfield model.
    """
    SavePerfunction(model.hurst, filename + "-hurst")
    SavePerfunction(model.topo, filename + "-topo")


def LoadTBfield(filename):
    """Load the tbfield model.

    :param str filename: File name (without extension).

    :returns: The field model.
    :rtype: tbfield
    """
    hurst = LoadPerfunction(filename + "-hurst")
    topo = LoadPerfunction(filename + "-topo")
    model = tbfield(filename, topo, hurst)

    return(model)


def SavePerfunction(func, filename):
    """Save the periodic function.

    :param str filename: File name (without extension).
    """
    with open(filename + ".pickle", "wb") as f:
        pickle.dump([func.ftype,
                     func.fname,
                     func.fparam,
                     func.finter,
                     func.steptrans,
                     func.trans,
                     func.translate,
                     func.rescale], f)


def LoadPerfunction(filename):
    """Load a periodic function from a file.

    :param str filename: File name (without extension).

    :returns: The periodic function.
    :rtype: perfunction
    """
    with open(filename + ".pickle", "rb") as f:
        Z = pickle.load(f)
    ftype = Z[0]
    name = Z[1]
    param = Z[2].size
    if "Fourier" in ftype:
        param = floor_divide(param, 2)
    model = perfunction(ftype, param, name)
    model.fparam[0, :] = Z[2][:]
    model.finter[0, :] = Z[3][:]
    model.steptrans = Z[4]
    model.trans = Z[5]
    model.translate = Z[6]
    model.rescale = Z[7]

    return(model)


def SaveSdata(self, filename):
    """Save an image in a file

    :param str filename: File name (without extension).
    """

    if self.coord.grid:
        with open(filename + ".pickle", "wb") as f:
            pickle.dump([self.M, self.values], f)
    else:
        print("sdata.Save: only available for images.")


def LoadSdata(filename):
    """Load an image from a file.

    :param str filename: File name (without extension).

    :returns: The image.
    :rtype: sdata
    """
    with open(filename + ".pickle", "rb") as f:
        Z = pickle.load(f)
    image = sdata()
    image.CreateImage(Z[0])
    image.values = Z[1]

    return(image)
