import microscotaspy.cell as mtcell
import skimage.io as skio

path = '/mnt/seaside/rsl/DataSetForTim/2D_Data/Kiwimagi12082017/CytationData/170811_112033_Plate 3/'

g = skio.imread(path + 'B6_02_2_6_GFP_001.tif')
r = skio.imread(path + 'B6_02_3_6_Texas Red_001.tif')
b = skio.imread(path + 'B6_02_4_6_TagBFP_001.tif')

# segment in green channel, compute intensities in red and blue with green mask
df = mtcell.get_events(g,(r,b),['g','r','b'])
