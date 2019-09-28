from collections import defaultdict
from BinaryReader import BinaryReader
from Ac7Base import Ac7Base
from Ac7Constants import *
from Ac7ParamList import Ac7ParamList

class Ac7Element(Ac7Base):
    def __init__(self):
        super().__init__()
        self.properties = defaultdict(lambda: defaultdict(lambda: {}))

    def _load(self, buffer, pos):
        self._buffer = buffer
        self._pos = pos
        magic = self._read(BinaryReader.magic("ELMT", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.u2le(self._buffer, self._pos))
        self._pos = Ac7ParamList()._load_parameter_list(self.properties["track_parameters"], self._buffer, self._pos)
        return self._pos