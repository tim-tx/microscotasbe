import sys

if not (sys.version_info.major == 3):
    raise ImportError("microscotaspy requires Python 3")

del sys
