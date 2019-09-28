from collections import defaultdict
from BinaryReader import BinaryReader
from Ac7Base import Ac7Base
from Ac7Element import Ac7Element
from Ac7ParamList import Ac7ParamList

class Ac7CommonParameters(Ac7Base):
    def __init__(self):
        super().__init__()
        self.properties = {'common_offset': 0,
                           'element_offsets': [],
                           'stylename': "",
                           'overall_parameters': defaultdict(lambda : {})
                           }

    def _load(self, buffer, pos, common_offset):
        self._buffer = buffer
        self._pos = pos
        self.properties['common_offset'] = common_offset
        #try to be smart about future file format changes, and set pos to common_offset now
        # in principle this should already be the case:
        if (self._pos != common_offset):
            print("Warning... expected to be at common offset, but something went wrong.\nPlease submit a bug report on github and attach your .ac7 file.")
        self._pos = self.properties['common_offset']
        # read magic number
        commontag = self._read(BinaryReader.magic(b'\xff\xff\xff\x07', None, self._buffer, self._pos))
        # read size
        size = self._read(BinaryReader.u2le(self._buffer, self._pos))
        # read element count
        element_count = self._read(BinaryReader.u1(self._buffer, self._pos))
        # read element offsets
        for i in range(element_count):
            offset = self._read(BinaryReader.u4le(self._buffer, self._pos))
            self.properties['element_offsets'].append(offset)
        # read dummy byte (end of offsets? seems to be always 0x00)
        self._read(BinaryReader.u1(self._buffer, self._pos))
        # read stylename length
        stylenamelength = self._read(BinaryReader.u1(self._buffer, self._pos))
        self.properties['stylename'] = self._read(BinaryReader.str(stylenamelength, "ascii", self._buffer, self._pos))
        # repeat reading parameters until no more params is read
        root_el = self.properties['overall_parameters']
        self._pos = Ac7ParamList()._load_parameter_list(root_el, self._buffer, self._pos)
        self.properties['overall_parameters']['elements'] = []
        for el in range(element_count):
            self.properties['overall_parameters']['elements'].append(Ac7Element())
            self._pos = self.properties['overall_parameters']['elements'][-1]._load(self._buffer, self._pos)

        #print(self.properties['overall_parameters']['elements'])

        return self._pos
