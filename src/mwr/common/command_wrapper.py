import os
import tempfile

class Wrapper(object):
    
    def _execute(self, argv):
        return os.spawnve(os.P_WAIT, argv[0], argv, os.environ)

    def _get_wd(self):
        return tempfile.mkdtemp()
        