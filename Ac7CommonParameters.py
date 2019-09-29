from collections import defaultdict
from BinaryReader import BinaryReader
from Ac7Base import Ac7Base
from Ac7Element import Ac7Element
from Ac7ParamList import Ac7ParamList
import struct

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
        self.properties['overall_parameters']['common'] = defaultdict(lambda:{})
        root_el = self.properties['overall_parameters']['common']
        self._pos = Ac7ParamList()._load_parameter_list(root_el, self._buffer, self._pos)
        self.properties['overall_parameters']['elements'] = []
        for el in range(element_count):
            self.properties['overall_parameters']['elements'].append(Ac7Element(el))
            self._pos = self.properties['overall_parameters']['elements'][-1]._load(self._buffer, self._pos)
        return self._pos

    def sanitize_stylename(self, stylename):
        newstylename = ''
        for c in stylename:
            if c in '!"#$\'()*+,-/:;<=>?0123456789 @ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}~':
                newstylename += c
        newstylename = newstylename[:12]
        return newstylename

    def _write(self, writer, buffer):
        buffer = writer.u4le(0x7fffffff, buffer, "start_of_commonparams")
        buffer = writer.u2le(0, buffer, "common_size")
        element_count = len(self.properties['overall_parameters']['elements'])
        buffer = writer.u1(element_count, buffer)
        for i in range(element_count):
            buffer = writer.u4le(0, buffer, "el_offset{0}".format(i))
        buffer = writer.u1(0, buffer)
        stylename = self.sanitize_stylename(self.properties['stylename'])
        buffer = writer.u1(len(stylename), buffer)
        buffer = writer.str(stylename, "ascii", buffer)
        root_el = self.properties['overall_parameters']
        buffer = Ac7ParamList()._write_parameter_list(root_el, writer, buffer)
        # fill in the bookmarks
        writer.set_bookmark("end_of_common_offset", len(buffer))
        size = writer.get_bookmark_position("end_of_common_offset") - writer.get_bookmark_position("start_of_commonparams")
        size_location = writer.get_bookmark_position("common_size")
        struct.pack_into("<H", buffer, size_location, size)
        return buffer



    def _summarize(self, title, result):
        result.append(title)
        result.append("*"*len(title))
        result.append("stylename: {0}".format(self.properties['stylename']))
        result.append("Overall parameters: {0}".format(self.properties['overall_parameters']['common'].items().__repr__()))
        for el in range(len(self.properties['overall_parameters']['elements'])):
            title = "Element {0}".format(el+1)
            self.properties['overall_parameters']['elements'][el]._summarize(title, result)
        return result