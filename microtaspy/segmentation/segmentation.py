import numpy as np
import pandas as pd
import scipy.ndimage as ndi
import skimage.filters as skfi
import skimage.measure as skmeas
import skimage.morphology as skmorph
import skimage.feature as skfeat
# import logging
# import time

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def segment(im):
    smooth = skfi.gaussian(im)
    t = skfi.threshold_otsu(smooth)
    smooth_thresh = smooth > t
    return smooth_thresh

def declump(im,mask):
    smooth = skfi.gaussian(im)
    local_maxi = skfeat.peak_local_max(smooth, indices=False, labels=mask, exclude_border=False)
    markers = skmeas.label(local_maxi)
    distance = ndi.distance_transform_edt(mask)
    labels_ws = skmorph.watershed(-distance, markers, mask=mask)
    return labels_ws

def _intensity(im,mask,level):
    cell_mask = np.where(mask == level)
    return np.mean(im[cell_mask])

def intensity(im,mask):
    levels = np.unique(mask)[1:]
    intensities = []
    for l in levels:
        intensities.append(np.mean(im[mask == l]))
    return np.array(intensities)

def get_events(im,layers=(),labels=('default',)):
    # assert(len(labels) == len(layers)+1)

    seg = segment(im)
    features = declump(im,seg)
    # logging.debug("Found %d events." % np.max(features))

    df = pd.DataFrame()
    for i,layer in enumerate(layers):
        df[labels[i]] = pd.Series(intensity(layer,features))

    return df,seg,features
