import unittest
import time
import logging
import microscotaspy.cell as mtcell
import skimage.io as skio
import numpy as np
import pandas as pd

class TestExtraction(unittest.TestCase):

    def test_extraction_time(self):
        path = '/mnt/seaside/rsl/DataSetForTim/2D_Data/Kiwimagi12082017/CytationData/170811_112033_Plate 3/'

        g = skio.imread(path + 'B5_02_2_6_GFP_001.tif')
        r = skio.imread(path + 'B5_02_3_6_Texas Red_001.tif')
        b = skio.imread(path + 'B5_02_4_6_TagBFP_001.tif')

        im = g
        layers = (r,b)
        labels = ['g','r','b']

        # segment in green channel, compute intensities in red and blue with green mask
        t0 = time.time()
        seg = mtcell.segment(im)
        t1 = time.time()
        logging.debug("Segmentation took %.3f seconds." % (t1-t0))

        t0 = time.time()
        features = mtcell.declump(im,seg)
        t1 = time.time()
        logging.debug("Declumping took %.3f seconds." % (t1-t0))
        logging.debug("Found %d events." % np.max(features))

        t0 = time.time()
        df = pd.DataFrame()
        for i,layer in enumerate((im,) + layers):
            df[labels[i]] = pd.Series(mtcell.intensity(layer,features))
        t1 = time.time()
        logging.debug("Intensity measurement took %.3f seconds." % (t1-t0))

    def test_get_events(self):
        path = '/mnt/seaside/rsl/DataSetForTim/2D_Data/Kiwimagi12082017/CytationData/170811_112033_Plate 3/'

        g = skio.imread(path + 'B5_02_2_6_GFP_001.tif')
        r = skio.imread(path + 'B5_02_3_6_Texas Red_001.tif')
        b = skio.imread(path + 'B5_02_4_6_TagBFP_001.tif')

        df = mtcell.get_events(g,(r,b),['g','r','b'])

if __name__ == '__main__':
    unittest.main()
