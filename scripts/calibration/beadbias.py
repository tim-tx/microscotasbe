import skimage.feature as feat
import skimage.io as skio
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndi
import skimage.exposure as skex
from scipy.interpolate import griddata
from glob import glob

path = "/mnt/seaside/rsl/DataSetForTim/Beads/170815_161237_SinglePeakBeads_liquid/170815_161237_Plate 1/"
beads_g_files = sorted(glob(path + "A1_*GFP*_001.tif"))

# screened by eye, ignoring big artifacts or images at the edge of the well
good = [0,1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,
        19,20,21,22,23,24,25,26,27,28,29,30,31,32]
beads_g = [skio.imread(f) for f in beads_g_files]
fig,ax = plt.subplots()

adj = []
for i in good:
    adj.append(skex.equalize_adapthist(skex.adjust_sigmoid(beads_g[i],cutoff=0.001,gain=30)))

blobs_log = []

for i in adj:
    blobs_log.append(feat.blob_log(i,threshold=0.05,min_sigma=5,max_sigma=8))

xi,yi = np.meshgrid(range(beads_g[0].shape[1]),range(beads_g[0].shape[0]))
intensity_g_flat = []
for j in range(len(blobs_log)):
    for i,blob in enumerate(blobs_log[j]):
        y,x,r = blob
        intensity_g_flat.append([y,x,np.mean(beads_g[good[j]][ (xi-x)**2 + (yi-y)**2 <= 2.5**2 ])]) 

n = 30                          # number of geometric bins
xi = np.linspace(0,beads_g[0].shape[1],n)
yi = np.linspace(0,beads_g[0].shape[0],n)
intensity_g_flat = np.array(intensity_g_flat)
grid_x, grid_y = np.mgrid[0:beads_g[0].shape[0]:50j, 0:beads_g[0].shape[1]:50j]
z = griddata(intensity_g_flat[:,:2],intensity_g_flat[:,2],(grid_x,grid_y),method='cubic')

z = np.zeros((n-1,n-1))
for j,y in enumerate(yi[1:]):
    for i,x in enumerate(xi[1:]):
        # a = np.logical_and((intensity_g_flat[:,0] < y),(intensity_g_flat[:,1] < x))
        # b = np.logical_and((intensity_g_flat[:,0] > yi[j]),(intensity_g_flat[:,1] > xi[i]))
        w = np.where(np.logical_and(np.logical_and((intensity_g_flat[:,0] < y),(intensity_g_flat[:,1] < x)),np.logical_and((intensity_g_flat[:,0] >= yi[j]),(intensity_g_flat[:,1] >= xi[i]))))[0]
        z[i,j] = np.mean(intensity_g_flat[w])
plt.imshow(z,extent=(0,1,0,1))
plt.show()

