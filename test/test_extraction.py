import unittest
import time
import logging
import microtaspy.segmentation as mseg
import skimage.io as skio
import numpy as np
import pandas as pd
from glob import glob

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestExtraction(unittest.TestCase):

    # def test_extraction_time(self):
    #     path = '/mnt/seaside/rsl/DataSetForTim/2D_Data/Kiwimagi12082017/CytationData/170811_112033_Plate 3/'

    #     g = skio.imread(path + 'B5_02_2_6_GFP_001.tif')
    #     r = skio.imread(path + 'B5_02_3_6_Texas Red_001.tif')
    #     b = skio.imread(path + 'B5_02_4_6_TagBFP_001.tif')

    #     im = g
    #     layers = (r,b)
    #     labels = ['g','r','b']

    #     # segment in green channel, compute intensities in red and blue with green mask
    #     t0 = time.time()
    #     seg = mseg.segment(im)
    #     t1 = time.time()
    #     logging.debug("Segmentation took %.3f seconds." % (t1-t0))

    #     t0 = time.time()
    #     features = mseg.declump(im,seg)
    #     t1 = time.time()
    #     logging.debug("Declumping took %.3f seconds." % (t1-t0))
    #     logging.debug("Found %d events." % np.max(features))

    #     t0 = time.time()
    #     df = pd.DataFrame()
    #     for i,layer in enumerate((im,) + layers):
    #         df[labels[i]] = pd.Series(mseg.intensity(layer,features))
    #     t1 = time.time()
    #     logging.debug("Intensity measurement took %.3f seconds." % (t1-t0))

    def test_get_events(self):
        import matplotlib.pyplot as plt
        path = 'data/'
        data = {}
        for chan in ['green','red','blue']:
            data[chan] = skio.imread_collection(sorted(glob(path + '%s_*.tif' % chan)))

        df = {}
        for chan in ['green','red','blue']:
            df[chan] = pd.DataFrame()
            for i in range(len(data[chan])):
                frame,seg,_ = mseg.get_events(data[chan][i],(data['green'][i],data['red'][i],data['blue'][i]),['g','r','b'])
                df[chan] = df[chan].append(frame)
            df[chan] = df[chan].reset_index(drop=True)
            # plt.imsave(chan + ".png",seg)
        # print(df)

if __name__ == '__main__':
    unittest.main()
