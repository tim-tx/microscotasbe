"""``microscotaspy`` is a tool to calibrate an optical microscope to
standard MEFLs units, and a collection of image processing routines
(utilizing scikit-image) to segment images of cells and test for
cell-cell contact.

The module is accordingly divided into two subpackages.

Subpackages
-----------
    :py:mod:`microscotaspy.calibrate`
        Characterize the microscope, following the TASBE protocol.
    :py:mod:`microscotaspy.cell`
        :mod:Image processing of cells.

"""

import sys

__version__ = '0.1'

if not (sys.version_info.major == 3):
    raise ImportError("microscotaspy requires Python 3")

del sys
