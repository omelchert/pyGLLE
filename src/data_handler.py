""" data_handler.py

Contains class data structure handling data accumulation and output.

AUTHOR: O. Melchert
DATE: 2020-01-17
"""
import os
import numpy as np


class DataHandler():
    """data structure holding accumulated data
    """
    def __init__(self, nSkip=1):
        """generates instance of data handler

        Attrib:
            w (numpy-array, ndim=1): anglular frequency axis
            t  (numpy-array, ndim=1): time axis
            z (numpy-array, ndim=1): z-axis, i.e. propagation direction axis
            u (numpy-array, ndim=2): frequency components of field
        """
        self.nSkip=nSkip
        self.Axt = []
        self.t = []
        self.x = []
        self.info = "00 -- I:INFO, D:DATA\n"

    def measure(self, n, t, x, Ax):
        """measure

        Callback function facilitating measurement

        Args:
            n (int): current propagation step
            t (numpy-array, ndim=1): time-axis
            x (numpy-array, ndim=1): x coordinate axis
            Ax (numpy-array, ndim=1): field components 
        """
        if n%self.nSkip==0:
            self.Axt.append(Ax)
            self.t.append(t)
            self.x = x

    def save(self, fName, path='./',**kwargs):
            """save data in numpy format

            Saves data in numpy native compressed npz format

            Args:
                oPath (str): path to folder where output will be stored
                fdBase (str): base name for output files
                Dat (object): data structure holding system data
                kwargs (dict): info dictionary
            """
            try:
                os.makedirs(path)
            except OSError:
                pass

            for key, val in sorted(kwargs.items()):
               self.info += "%s: %s\n"%(key,val)

            with open(path + fName + '.npz', 'w') as f:
                np.savez_compressed(f,
                        info=self.info,
                        x=np.asarray(self.x),
                        t=np.asarray(self.t),
                        Axt=np.asarray(self.Axt))

# EOF: data_handler.py 
