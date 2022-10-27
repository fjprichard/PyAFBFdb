#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Class for managing database of simulated AFBF with
random topothesy and Hurst functions.

.. codeauthor:: Frédéric Richard <frederic.richard_at_univ-amu.fr>
"""
import pickle
import time
import os

from afbf.utilities import seed, set_state, get_state
from afbf.utilities import zeros, pi, array, append, arange, nonzero, sort
from afbf import tbfield, perfunction, sdata, coordinates
from afbfdb.ClassesIO import LoadPerfunction, LoadSdata
from afbfdb.ClassesIO import SaveTBfield, SaveSdata


class protocol:
    """This class enables to manage and build database.

    :param str rep: Path to the data directory.
    :param int M:
        Number of parameters for the Hurst and topothesy functions.
    :param str smode_cst:
        Mode of simulation of the Hurst and topothesy function.
    :param float Hmin:
        Minimal value of the Hurst index in :math:`(0, 1)`.
    :param float Hmax:
        Maximal value of the Hurst index in :math:`(0, 1)`.
    :param str smode_int:
        Mode of simulation of the intervals of the Hurst function.
    :param float dint:
        Minimal interval lenght of the Hurst function steps.
    :param int K: Number of turning bands.
    :param int N: image size.
    """

    def __init__(self, rep="SimulationSet_001", M=2,
                 smode_cst="unifmin", Hmin=0.01, Hmax=0.99,
                 smode_int="nonunif", dint=0.001, K=500, N=64):
        """Set the protocol.

        :param str rep: Path to the data directory.
        :param int M:
            Number of parameters for the Hurst and topothesy functions.
        :param str smode_cst:
            Mode of simulation of the Hurst and topothesy function.
        :param float Hmin:
            Minimal value of the Hurst index in :math:`(0, 1)`.
        :param float Hmax:
            Maximal value of the Hurst index in :math:`(0, 1)`.
        :param str smode_int:
            Mode of simulation of the intervals of the Hurst function.
        ;param float dint:
            Minimal interval lenght of the Hurst function steps.
        :param int K: Number of turning bands.
        :param int N: image size.
        """
        self.rep = rep
        if os.path.isdir(self.rep):
            print('Load an existing protocol.')
            self.LoadSetting()
        else:
            os.mkdir(self.rep)
            print("Define a new protocol.")
            self.nbexpe = None
            self.K = K
            self.M = M
            self.N = N
            self.smode_cst = smode_cst
            self.Hmin = Hmin
            self.Hmax = Hmax
            self.smode_int = smode_int
            self.dint = dint

            # Save setting.
            with open(self.rep + "/setting.pickle", "wb") as f:
                pickle.dump([self.K, self.M, self.N, self.smode_cst,
                             self.Hmin, self.Hmax, self.smode_int,
                             self.dint], f)

            self.nbexpe = 0
            self.DataConsistency = True

            # Define a random state and save it.
            rs = get_state()
            filename = self.rep + "/randomstate.pickle"
            with open(filename, "wb") as f:
                pickle.dump([rs], f)

        self.n = 0

        if self.DataConsistency:
            # Field definition.
            hurst = perfunction("step-smooth", self.M, "Hurst")
            topo = perfunction("step-smooth", self.M, "Topothesy")
            self.field = tbfield("Field", topo, hurst)
            self.field.InitTurningBands(self.K)  # Turning band initialization.

            # Image definition.
            self.coord = coordinates(self.N)  # Image coordinates.
            self.X = sdata()
            self.X.coord = self.coord
            self.X.name = "Example"

            self.DisplaySetting()

    def DisplaySetting(self):
        """Display the setting of the protocol.
        """
        print("Protocol:")
        print("Directory:" + self.rep)
        print("Number of examples: %d" % (self.nbexpe))
        print("Image size: %d x %d" % (self.N, self.N))
        print("Hurst function:")
        print("Number of parameters: %d" % (self.M))
        print("Step constant sampling: " + self.smode_cst)
        print("Step interval sampling: " + self.smode_int)
        print("Minimal Hurst value: %-3.2f" % (self.Hmin))
        print("Maximal Hurst value: %-3.2f" % (self.Hmax))
        print("Minimal interval lenght between steps: %3.2f" % (self.dint))
        print("Number of turning bands: %d" % (self.K))

    def LoadSetting(self):
        """Load the protocol setting.
        """
        self.CheckConsistency()
        if self.DataConsistency:
            with open(self.rep + "/setting.pickle", "rb") as f:
                Z = pickle.load(f)
                self.K = Z[0]
                self.M = Z[1]
                self.N = Z[2]
                self.smode_cst = Z[3]
                self.Hmin = Z[4]
                self.Hmax = Z[5]
                self.smode_int = Z[6]
                self.dint = Z[7]

    def CheckConsistency(self):
        """Check the consistency of the database.
        """
        self.DataConsistency = True
        setting = False
        randomstate = False
        image = array([])
        hurst = array([])
        topo = array([])
        feat = array([])
        files = os.listdir(self.rep)
        for j in range(len(files)):
            file = files[j]
            if file.find("example") >= 0:
                n = int(file[8:14])
                if file.find("-image", 0) >= 0:
                    image = append(image, n)
                elif file.find("-hurst", 0) >= 0:
                    hurst = append(hurst, n)
                elif file.find("-topo", 0) >= 0:
                    topo = append(topo, n)
                elif file.find("-features", 0) >= 0:
                    feat = append(feat, n)
            elif file == "setting.pickle":
                setting = True
            elif file == "randomstate.pickle":
                randomstate = True

        n = min(array([image.size, hurst.size, topo.size, feat.size]))
        exam = arange(0, n)
        image = sort(image)
        topo = sort(topo)
        hurst = sort(hurst)
        feat = sort(feat)
        ind = nonzero(exam - image[0:n] != 0)
        if ind[0].size != 0:
            print("Missing images:", ind[0])
        ind = nonzero(exam - topo[0:n] != 0)
        if ind[0].size != 0:
            print("Missing topothesy:", ind[0])
        ind = nonzero(exam - hurst[0:n] != 0)
        if ind[0].size != 0:
            print("Missing Hurst:", ind[0])
        ind = nonzero(exam - feat[0:n] != 0)
        if ind[0].size != 0:
            print("Missing features:", ind[0])

        if image.size > n or topo.size > n or hurst.size > n or feat.size > n:
            print("Unequal number of example data.")
            print("Data limited to " + str(n - 1))

        self.nbexpe = n

        if setting is False:
            print("Setting file: missing.")
            self.DataConsistency = False

        if randomstate is False:
            print("Random state: missing.")
            self.DataConsistency = False

        if self.DataConsistency is not True:
            print("Setting failed due to inconsistent data.")

    def SetFileName(self, n):
        """Set the name of the file of an example.
        """
        filename = str(1000000 + n)
        filename = self.rep + "/example-" + filename[1:]

        return filename

    def LoadExample(self, n):
        """Load an example.

        :param int n: The index of the example.
        """
        if self.DataConsistency is not True:
            print("LoadExample: set the database.")
            return(-1)

        if n >= self.nbexpe:
            print("LoadExample: index %d out of bounds." % (n))
            return(0)

        self.n = n
        filename = self.SetFileName(n)
        self.field.name = "Field " + str(n)
        self.field.hurst = LoadPerfunction(filename + "-hurst")
        self.field.topo = LoadPerfunction(filename + "-topo")
        self.X = LoadSdata(filename + "-image")
        self.X.name = "Example " + str(n)
        with open(filename + "-features.pickle", "rb") as f:
            Z = pickle.load(f)
        self.field.H = Z[0]
        self.field.hurst_argmin_lenght = Z[1]
        self.field.hurst_argmin_center = Z[2]

        return(1)

    def SaveExample(self):
        """Save an example.

        :param int n: The index of the example.
        """
        filename = self.SetFileName(self.n)
        SaveSdata(self.X, filename + "-image")
        SaveTBfield(self.field, filename)
        with open(filename + "-features.pickle", "wb") as f:
            pickle.dump([self.field.H,
                         self.field.hurst_argmin_lenght,
                         self.field.hurst_argmin_center], f)

    def ShowExample(self, n=None):
        """Show an example.

        :param int n: The index of the example.
        """
        if n is None:
            n = self.n
        err = self.LoadExample(n)
        if err > 0:
            self.field.DisplayParameters(3 * n + 1)
            self.X.Display(3 * n + 3)
            print("Example %d" % (self.n))
            print("Hurst-related parameters:")
            print("min = %3.2f, argmin length = %3.2f and center = %3.2f"
                  % (self.field.H, self.field.hurst_argmin_lenght,
                     self.field.hurst_argmin_center))

    def SetRandomState(self):
        """Set the random state used for simulations.
        """
        filename = self.rep + "/randomstate.pickle"
        with open(filename, "rb") as f:
            Z = pickle.load(f)
            set_state(Z[0])

    def SimulateFields(self, expe_start=0, expe_end=99,
                       _save=True, _display=False):
        """Simulate a series of random fields.
        """
        if self.DataConsistency is not True:
            print("SimulateFields: set the protocol.")

        # Load the random state.
        filename = self.rep + "/randomstate.pickle"
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                Z = pickle.load(f)
            rs = Z[0]
            set_state(rs)

        # Set the mode of simulation.
        self.field.hurst.SetStepSampleMode(self.smode_cst,
                                           self.Hmin, self.Hmax,
                                           self.smode_int, self.dint)

        print("Field simulation:")
        print("From example " + str(expe_start) + " to " + str(expe_end))
        print("Save option:" + str(_save))
        if _save:
            print("to directory:" + str(self.rep))
        print("Display option:" + str(_display))

        start = time.time()
        for n in range(expe_start, expe_end + 1):
            self.n = n
            seed(n)
            # Define a new model.
            self.field.hurst.ChangeParameters()
            self.field.NormalizeModel()
            # Compute some model features.
            self.field.ComputeFeatures_Hurst()
            # Simulate the field
            seed(n)
            self.X = self.field.Simulate(self.coord)
            if _save is True:
                self.SaveExample()

            if _display is True:
                print("Example %d: %4.3f sec." % (n, time.time() - start))
                start = time.time()
                self.ShowExample()
        self.nbexpe = expe_end + 1

    def ExportData(self, n_start=0, n_end=None):
        """Export the data.

        :param int n_start: first example.
        :param int n_end: last example.

        :returns: (images, features)
        :rtype: (ndarrays, ndarrays)

        .. note::
            - images is an array of size N x N x (n_end - n_start + 1):
              images[j, :, :] is the image of the (n_start + j)th example.
            - features, an array of size N x N x (n_end - n_start + 1):
              features[j, :] are the features of the (n_start +j)th examples.

              * features[j, 0] is the Hurst index.
              * features[j, 1] is the lenght of the Hurst argmin set.
              * features[j, 2] is the center of the Hurst argmin set.

        """
        if self.DataConsistency is not True:
            print("ExportData: set the database.")
            return(-1)
        if n_end is None:
            n_end = self.nbexpe - 1

        nbexamples = n_end - n_start + 1
        images = zeros((nbexamples, self.N, self.N), dtype=float)
        features = zeros((nbexamples, 3), dtype=float)
        for j in range(n_start, n_end + 1):
            j0 = j - n_start
            self.LoadExample(j)
            images[j0, :, :] =\
                self.X.values.reshape(self.X.M)[:, :]
            features[j0, 0] = self.field.H
            features[j0, 1] = self.field.hurst_argmin_lenght
            features[j0, 2] = self.field.hurst_argmin_center

        return(images, features)


def Protocol_001(rep="SimulationSet_001", N=64):
    """A protocol to manage database of simulations of random fields.

    In this protocol the Hurst index, the length and the center of
    the argmin set of the Hurst function are uniformly sampled.


    :param str rep: directory of the database.
    :param int nbexpe: optional
        Last element of the database. The default is 1000.
    :param int N : optional
        Image size. The default is 256.

    :returns: The protocol to deal with the database.
    :rtype: protocol.
    """

    K = 500  # Number of bands.
    M = 2  # Number of steps in the Hurst and topothesy functions.

    smode_cst = "unifmin"  # Mode of simulation of step constants.
    Hmin = 0.05  # Minimal value for the Hurst function.
    Hmax = 0.95  # Maximal value for the Hurst function.

    smode_int = "nonunif"  # Mode of simulation of step intervals.
    dint = pi / 100.0  # Minimal length of intervals of the Hurst function.

    # Set the database used for training and testing.
    simu = protocol(rep, M, smode_cst, Hmin, Hmax, smode_int, dint, K, N)

    return simu
