from collections import defaultdict
from BinaryReader import BinaryReader
from Ac7Base import Ac7Base
from Ac7Constants import *
from Ac7ParamList import Ac7ParamList

class Ac7Element(Ac7Base):
    def __init__(self, el):
        super().__init__()
        self.properties = defaultdict(lambda: defaultdict(lambda: {}))
        self.el = el
        self.el_interpreted = { 0 : "intro", 1: "normal", 2: "variation", 3:"normal fill-in", 4:"variation fill-in", 5: "ending",
                                6 : "intro 2",  7 : "ending 2", 8 : "fill 2", 9: "fill 4" }[el]

    def _load(self, buffer, pos):
        self._buffer = buffer
        self._pos = pos
        magic = self._read(BinaryReader.magic("ELMT", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.read("u2le", self._buffer, self._pos))
        self._pos = Ac7ParamList()._load_parameter_list(self.properties["track_parameters"], self._buffer, self._pos)
        return self._pos

    def _summarize(self, title, result):
        longtitle = title + " ({0})".format(self.el_interpreted)
        result.append(longtitle)
        result.append("-" * len(longtitle))
        for prop in self.properties['track_parameters']:
            result.append("Property: {0}".format(prop))
            result.append("          {0}".format(self.properties['track_parameters'][prop].__repr__().replace("}, ", "\n")))
        return result