import sys
import os
import numpy as np
import scipy.fftpack as sfft
from figure_base_propagationDynamics import generateFigure


def fetchNpz(iPath):
    data = np.load(iPath)
    x = data['x']
    k = sfft.fftfreq(x.size,d=x[1]-x[0])*2*np.pi
    t = data['t']
    Axt = data['Axt']
    return x, k, t, Axt


def main():

    inFile = sys.argv[1]

    (x,k,t,At) = fetchNpz(inFile)
    xLim = (-8,8)
    xTicks = (-8,-4,0,4,8)
    tLim = (0,5.)
    tTicks = (0,1,2,3,4,5)
    kLim = (-65,65)
    kTicks = (-60,-40,-20,0,20,40,60)

    path, inFileName = os.path.split(inFile)
    inFileBasename = os.path.splitext(inFileName)[0]

    generateFigure(x,k,t,At,xLim,xTicks,kLim,kTicks,tLim,tTicks,inFileBasename,DO_FORMAT='png')


main()
