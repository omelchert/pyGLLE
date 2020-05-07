import sys
import os
import matplotlib as mpl
import numpy as np
import scipy.fftpack as sfft
import matplotlib.pyplot as plt
import matplotlib.colors as col
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


def fetchIdx(t,t0):
    return np.argmin(np.abs(t-t0))

def generateFigure():

    mm2inch = lambda x: x/10./2.54
    mpl.rcParams['figure.figsize'] = mm2inch(85),mm2inch(1.8/3.*85)
    mpl.rcParams['xtick.direction']= 'out'
    mpl.rcParams['ytick.direction']= 'out'
    mpl.rcParams['xtick.labelsize'] = 6
    mpl.rcParams['ytick.labelsize'] = 6
    mpl.rcParams['lines.linewidth'] = 1.0
    mpl.rcParams['axes.linewidth'] = 0.5
    mpl.rcParams['axes.labelsize'] = 6
    mpl.rcParams['font.size'] = 6
    mpl.rcParams['legend.fontsize'] = 6

    mpl.rcParams['text.usetex'] = True
    mpl.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
    ]

    cmap=mpl.cm.get_cmap('jet')

    fig = plt.figure()
    plt.subplots_adjust(left=0.1, bottom=0.14, right=0.98, top= 0.98, wspace=0.45, hspace=0.3)

    gs00 = GridSpec(1,1)
    gsA = GridSpecFromSubplotSpec(2,1,subplot_spec=gs00[0,0],wspace=0.1, hspace=0.1)
    axA1 = plt.subplot(gsA[0,0])
    axA2 = plt.subplot(gsA[1,0])

    def _setKey(ax, lns, ncol=2):
        """key helper"""
        labs = [l.get_label() for l in lns]
        lg = ax.legend(lns, labs, title=r"", loc=1, fontsize=6, ncol=ncol)
        lg = ax.legend_
        lg.get_frame().set_linewidth(0.5)

    inFile = '../data_stationary_solution/stationary_solution.dat.npz'
    (x, Ax_ini, Ax_opt) = fetchNpz(inFile)

    xLim = (-3.,3.)
    xTicks = (-3,-2,-1,0,1,2,3)

    l1 = axA1.plot(x,np.abs(Ax_ini), color='red', dashes=[2,2], label=r'$|A_{\rm{trial}}(x)|$',zorder=1)
    l2 = axA1.plot(x,np.abs(Ax_opt), color='k', label=r'$|A_{\rm{opt}}(x)|$',zorder=0)

    axA1.xaxis.set_ticks_position('bottom')
    axA1.yaxis.set_ticks_position('left')
    axA1.tick_params(axis='y',length=2.,pad=1)
    axA1.tick_params(axis='x',length=2.,pad=1,labelbottom=False)
    axA1.set_xlim(xLim)
    axA1.set_xticks(xTicks)
    axA1.set_ylim(0,6.5)
    axA1.set_yticks((0,2,4,6))

    _setKey(axA1,l1+l2,1)

    l1 = axA2.plot(x,np.real(Ax_ini), color='red', label=r'$\sf{Re}[A_{\rm{trial}}(x)]$',zorder=1)
    l2 = axA2.plot(x,np.real(Ax_opt), color='k', label=r'$\sf{Re}[A_{\rm{opt}}(x)]$',zorder=0)

    l3 = axA2.plot(x,np.imag(Ax_ini), color='red', dashes=[2,2], label=r'$\sf{Im}[A_{\rm{trial}}(x)]$',zorder=1)
    l4 = axA2.plot(x,np.imag(Ax_opt), color='k', dashes=[2,2], label=r'$\sf{Im}[A_{\rm{opt}}(x)]$',zorder=0)

    axA2.xaxis.set_ticks_position('bottom')
    axA2.yaxis.set_ticks_position('left')
    axA2.tick_params(axis='y',length=2.,pad=1)
    axA2.tick_params(axis='x',length=2.,pad=1)
    axA2.set_xlim(xLim)
    axA2.set_xticks(xTicks)
    axA2.set_ylim(-2,6.5)
    axA2.set_yticks((-2,0,2,4,6))
    axA2.set_xlabel(r'$x$')

    _setKey(axA2,l1+l3+l2+l4,1)

    DO_FORMAT='png'
    if DO_FORMAT=='png':
        fName = './FIGS/stationarySolution.png'
        plt.savefig(fName,format='png',dpi=600)
    elif DO_FORMAT=='svg':
        fName = './SVGS/stationarySolution.svg'
        plt.savefig(fName,format='svg',dpi=600)
    else:
        fName = './FIGS/stationarysolution.png'
        print('# saved under:', fName)
        plt.savefig(fName,format='png',dpi=600)



def fetchNpz(iPath):
    data = np.load(iPath)
    x = data['x']
    Ax_ini = data['Ax0_ini']
    Ax_opt = data['Ax0']
    return x, Ax_ini, Ax_opt


def main():
    generateFigure()


main()
