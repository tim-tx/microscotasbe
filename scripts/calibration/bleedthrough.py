# This file reads all the images and generates bleedthrough
# plots. It's fairly slow, I think the bottleneck is in
# microtaspy.cell.intensity().

import microtaspy.cell as mtcell
import microtaspy.calibrate as mtcalib

import logging
import skimage.io as skio
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

path = "/mnt/seaside/rsl/DataSetForTim/11042016synNotch/CitationData/161104_083217_synNotch/161104_085013_Plate 2/"

controls = {'r':'C4','g':'B4','b':'D4'} # these are well labels

# build dictionary so we can ask for bleedthrough from red to green like mydict['r']['g']
d = dict.fromkeys(['r','g','b'])
intensities = d.copy()
for k in intensities.keys():
    intensities[k] = d.copy()

for c in controls.keys():
    logging.info('well %s' % controls[c])

    temp_intensities = {'r':[],'g':[],'b':[]}
    for j in range(4):          # stitch number
        logging.info('stitch number %d' % (j+1))
        r = skio.imread(path + controls[c] + '_03_3_%d_Texas Red_%03d.tif' % (j+1,1))
        g = skio.imread(path + controls[c] + '_03_2_%d_GFP_%03d.tif' % (j+1,1))
        b = skio.imread(path + controls[c] + '_03_4_%d_TagBFP_%03d.tif' % (j+1,1))
        images = {'r':r,'g':g,'b':b}

        seg = mtcell.segment(images[c])
        labels = mtcell.declump(images[c],seg)

        for key in temp_intensities.keys():
            temp_intensities[key].append(mtcell.intensity(images[key],labels))

    for key in intensities.keys():
        intensities[c][key] = np.hstack(temp_intensities[key])

bins = d.copy()
for k in bins.keys():
    bins[k] = dict.fromkeys(bins.keys())

fig = plt.figure(figsize=(10,12))

labels = {'r':'red intensity','g':'green intensity','b':'blue intensity'}

for i,fromchan in enumerate(bins.keys()):
    for j,tochan in enumerate(bins[fromchan].keys()):
        intensities[fromchan][tochan]
        a = np.log10(np.min(intensities[fromchan][tochan]))
        b = np.log10(np.max(intensities[fromchan][tochan]))
        bins[fromchan][tochan] = np.logspace(a,b,75)

# could adjust bins here to keep y axes the same for a given row in
# the plots
        
for i,fromchan in enumerate(bins.keys()):
    otherchans = list(bins[fromchan].keys())
    otherchans.remove(fromchan)
    for j,tochan in enumerate(otherchans):
        ax = fig.add_axes([0.1+j*0.4,0.7-i*0.3,0.3,0.25])
        bldthru = (intensities[fromchan][fromchan],intensities[fromchan][tochan])
        label_list = (labels[fromchan],labels[tochan])
        bin_list = [bins[fromchan][fromchan],bins[fromchan][tochan]]
        hist = mtcalib.bleedthrough_heatmap(bldthru,label_list,bin_list,ax=ax)
        # np.savetxt('%s-%s.txt' % (fromchan,tochan),hist)

plt.show()
# plt.savefig()
