from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy.ndimage as ndi
import skimage.filters as skfi
import skimage.measure as skmeas
import skimage.morphology as skmorph

from ..cell import segment,declump

def bleedthrough_scatter(intensities,labels,ax=None):
    if ax is None:
        ax = plt.gca()

    ax.scatter(intensities[0],intensities[1],s=1)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

def bleedthrough_heatmap(intensities,labels,bins,ax=None):
    H, xedges, yedges = np.histogram2d(intensities[0],intensities[1],bins=bins)
    H = H.T
    if ax is None:
        ax = plt.gca()

    X,Y = np.meshgrid(xedges,yedges)
    ax.pcolor(X,Y,H,cmap=cm.jet)
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    
    return(H)
