class Ac7Base(object):
    def __init__(self):
        self._buffer = None
        self._pos = 0

    def _read(self, retval_inc):
        retval, newpos = retval_inc
        self._pos = newpos
        return retval