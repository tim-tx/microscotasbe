import numpy as np
import pandas as pd
import scipy.ndimage as ndi
import skimage.filters as skfi
import skimage.measure as skmeas
import skimage.morphology as skmorph
import skimage.feature as skfeat

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

def intensity(im,mask):
    levels = np.unique(mask)[1:]
    intensities = []
    for l in levels:
        cell_mask = np.where(mask == l)
        intensities.append(np.mean(im[np.where(mask == l)]))
    return np.array(intensities)

def get_events(im,layers=(),labels=('default',)):
    assert(len(labels) == len(layers)+1)
    seg = segment(im)
    features = declump(im,seg)
    df = pd.DataFrame({labels[0]: intensity(im,features)})
    for i,layer in enumerate(layers):
        df[labels[i+1]] = pd.Series(intensity(layer,features))
    return df
