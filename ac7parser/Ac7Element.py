from collections import defaultdict

from .Ac7Base import Ac7Base
from .Ac7ParamList import Ac7ParamList
from .BinaryReader import BinaryReader
from .Ac7Constants import ac7elements


class Ac7Element(Ac7Base):
    def __init__(self, el):
        super().__init__()
        self.properties = defaultdict(lambda: [])
        self.el = el
        self.lut = ac7elements
        elems_in_lut = len(self.lut)
        for i in range(20):
            self.lut[i + elems_in_lut] = "unknown element type {0}".format(i)
        self.el_interpreted = self.lut[el]

    def _load(self, buffer, pos):
        self._buffer = buffer
        self._pos = pos
        magic = self._read(BinaryReader.magic("ELMT", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.read("u2le", self._buffer, self._pos))
        self.properties["track_parameters"] = []
        self._pos = Ac7ParamList()._load_parameter_list(self.properties["track_parameters"], self._buffer, self._pos)
        return self._pos

    def _write(self, buffer, writer, index_prefix, index):
        buffer = writer.str("ELMT", "ascii", buffer, "start_of_{0}{1}".format(index_prefix, index))
        buffer = writer.write("u2le", 0, buffer, "{0}_offset_{1}".format(index_prefix, index))  # size
        buffer = Ac7ParamList()._write_parameter_list(self.properties["track_parameters"], writer, buffer)
        end_of_el = len(buffer)
        buffer = writer.write_into("{0}_offset_{1}".format(index_prefix, index),
                                   end_of_el - writer.get_bookmark_position(
                                       "{0}_offset_{1}".format(index_prefix, index)) + 4,
                                   buffer)
        return buffer

    def _summarize(self, title, result):
        longtitle = title + " ({0})".format(self.el_interpreted)
        result.append(longtitle)
        result.append("-" * len(longtitle))
        for prop in self.properties['track_parameters']:
            result.append("Property: {0}".format(prop['parm']))
            result.append("          {0}".format(prop.__repr__().replace("}, ", "},\n")))
        return result
