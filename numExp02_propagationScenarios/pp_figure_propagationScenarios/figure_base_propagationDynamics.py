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

def generateFigure(x, k, t, At, xLim, xTicks, kLim, kTicks, tLim, tTicks, oName, DO_FORMAT='png'):

    mm2inch = lambda x: x/10./2.54
    mpl.rcParams['figure.figsize'] = mm2inch(1.*85),mm2inch(1.3/3.*85)
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

    #cmap=mpl.cm.get_cmap('CMRmap')
    #cmap=mpl.cm.get_cmap('gnuplot')
    cmap=mpl.cm.get_cmap('jet')

    fig = plt.figure()
    plt.subplots_adjust(left=0.08, bottom=0.19, right=0.98, top= 0.8, wspace=0.45, hspace=0.05)

    gs00 = GridSpec(1,1)
    gsA = GridSpecFromSubplotSpec(6,5,subplot_spec=gs00[0,0],wspace=0.1, hspace=0.1)
    axA1 = plt.subplot(gsA[1:,0:2])
    axA2 = plt.subplot(gsA[1:,2:])
    axA1t = plt.subplot(gsA[0,0:2])
    axA2t = plt.subplot(gsA[0,2:])

    # -- SUBPLOT: X-DOMAIN 

    def _colorbar_Ix(im,refPos,refPos2):
        """colorbar helper"""
        x0, y0, w, h = refPos.x0, refPos.y0, refPos.width, refPos.height
        x2, y2, w2, h2 = refPos2.x0, refPos2.y0, refPos2.width, refPos2.height
        cax = fig.add_axes([x0, y0+1.05*h+h2, w, 0.065*h])
        cbar = fig.colorbar(im, cax=cax, orientation='horizontal', extend='max')
        cbar.ax.tick_params(color='k',
                            labelcolor='k',
                            bottom=False,
                            direction='out',
                            labelbottom=False,
                            labeltop=True,
                            top=True,
                            size=2,
                            labelsize=4.5,
                            pad=-1.
                            )

        cbar.set_ticks((0,0.2,0.4,0.6,0.8,1.))
        return cbar

    Ix =  np.abs(At)**2
    Ix = Ix/Ix[0].max()
    img1 = axA1.pcolorfast(x,t,Ix[:-1,:-1],norm=col.Normalize(vmin=0.,vmax=1.0),cmap=cmap)
    cbar1 = _colorbar_Ix(img1,axA1.get_position(), axA1t.get_position() )
    cbar1.ax.set_title(r"Normalized intensity $|A|^2$",color='k',fontsize=6., y=2.)
    axA1.tick_params(axis='both',length=2.,pad=1)
    axA1.xaxis.set_ticks_position('bottom')
    axA1.yaxis.set_ticks_position('left')
    axA1.set_xlim(xLim)
    axA1.set_xticks(xTicks)
    axA1.set_xlabel(r"$x$")
    axA1.set_ylim(tLim)
    axA1.set_yticks(tTicks)
    axA1.set_ylabel(r"$t$")


    # -- SUBPLOT: K-DOMAIN

    def _colorbar_Ik(im,refPos,refPos2):
            """colorbar helper"""
            x0, y0, w, h = refPos.x0, refPos.y0, refPos.width, refPos.height
            x2, y2, w2, h2 = refPos2.x0, refPos2.y0, refPos2.width, refPos2.height
            cax = fig.add_axes([x0, y0+1.05*h+h2, w, 0.065*h])
            cbar = fig.colorbar(im, cax=cax, orientation='horizontal')
            cbar.ax.tick_params(color='k',
                                labelcolor='k',
                                bottom=False,
                                direction='out',
                                labelbottom=False,
                                labeltop=True,
                                top=True,
                                size=2,
                                labelsize=4.5,
                                pad=-1.
                                )

            dBLabels = np.asarray([-150,-120,-90,-60,-30,0])
            _fromdB = lambda x: 10.**(0.1*x)
            cbar.set_ticks(_fromdB(dBLabels))
            cbar.set_ticklabels(dBLabels)
            return cbar

    Ak = sfft.ifft(At,axis=-1)
    Ik = np.abs(Ak)**2
    Ik = Ik/Ik[0].max()
    img2 = axA2.pcolorfast(sfft.fftshift(k),t, sfft.fftshift(Ik[:-1,:-1],axes=-1), norm=col.LogNorm(vmin=1e-15,vmax=1.0),cmap=cmap)
    cbar1 = _colorbar_Ik(img2,axA2.get_position(), axA2t.get_position())
    cbar1.ax.set_title(r"Normalized spectral intensity $|A_k|^2\,\mathrm{(dB)}$",color='k',fontsize=6., y=2.)

    axA2.xaxis.set_ticks_position('bottom')
    axA2.yaxis.set_ticks_position('left')
    axA2.xaxis.set_ticks_position('bottom')
    axA2.yaxis.set_ticks_position('left')
    axA2.tick_params(axis='y',length=2.,pad=1,labelleft=False)
    axA2.tick_params(axis='x',length=2.,pad=1)
    axA2.set_xlim(kLim)
    axA2.set_xticks(kTicks)
    axA2.set_xlabel(r"$k$")
    axA2.set_ylim(tLim)
    axA2.set_yticks(tTicks)

    # -- SUBPLOT: INTENSITY AT FINAL SLICE

    tFinId = fetchIdx(t,tLim[1])

    Ax_fin = np.copy(At[tFinId])
    Ix_fin = np.abs(Ax_fin)**2
    Ix_fin /= np.max(Ix_fin)

    axA1t.plot(x,Ix_fin,color='black',linewidth=0.5)

    axA1t.tick_params(axis='y',length=2.,pad=1,labelleft=False)
    axA1t.tick_params(axis='x',length=2.,pad=1,labelbottom=False)
    axA1t.set_xlim(xLim)
    axA1t.set_xticks(xTicks)
    axA1t.set_ylim(-0.02,1.02)
    axA1t.spines['left'].set_visible(False)
    axA1t.spines['right'].set_visible(False)
    axA1t.spines['top'].set_visible(False)
    axA1t.spines['bottom'].set_visible(False)
    axA1t.tick_params(axis='x',bottom=False,top=False)
    axA1t.tick_params(axis='y',left=False,right=False)

    # -- SUBPLOT: SPECTRAL INTENSITY AT FINAL SLICE

    def dB(x):
        return 10.*np.log10(x)

    Ak_fin = np.copy(Ak[tFinId])
    Ik_fin = np.abs(Ak_fin)**2
    Ik_fin /= np.max(Ik_fin)

    #axA2t.vlines(sfft.fftshift(k),-150,dB(sfft.fftshift(Ik_fin)),color='black',linewidth=0.5)
    axA2t.plot(sfft.fftshift(k),dB(sfft.fftshift(Ik_fin)),color='black',linewidth=0.5)

    axA2t.tick_params(axis='y',length=2.,pad=1,labelleft=False)
    axA2t.tick_params(axis='x',length=2.,pad=1,labelbottom=False)
    axA2t.set_xlim(kLim)
    axA2t.set_xticks(kTicks)
    axA2t.set_ylim(-150,0.)
    axA2t.set_yticks((-150,-100.,-50,0))
    axA2t.spines['left'].set_visible(False)
    axA2t.spines['right'].set_visible(False)
    axA2t.spines['top'].set_visible(False)
    axA2t.spines['bottom'].set_visible(False)
    axA2t.tick_params(axis='x',bottom=False, top=False)
    axA2t.tick_params(axis='y',left=False, right=False)

    #for i in range(k.size):
    #    print k[i], Ik_fin[i]
    #exit()


    if DO_FORMAT=='png':
        fName = './FIGS/'+oName+'.png'
        plt.savefig(fName,format='png',dpi=600)
    elif DO_FORMAT=='svg':
        fName = './SVGS/'+oName+'.svg'
        plt.savefig(fName,format='svg',dpi=600)
    else:
        fName = './FIGS/'+oName+'.png'
        print '# saved under:', fName
        plt.savefig(fName,format='png',dpi=600)

