from BinaryReader import BinaryReader
from Ac7Base import Ac7Base
from Ac7Constants import *

class Ac7ParamList(Ac7Base):
    def __init__(self):
        self._buffer = None
        self._pos = 0

    def _load_parameter_list(self, root_el, buffer, pos):
        self._buffer = buffer
        self._pos = pos
        param_id = self._read(BinaryReader.u1(self._buffer, self._pos))
        while param_id != ac7paramnomore:
            if param_id == ac7parambeat:
                length = self._read(BinaryReader.u1(self._buffer, self._pos))
                parm = 'param_beat'
                root_el[parm]["length"] = length
                beat = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
                root_el[parm]["beat_nominator"] = beat >> 4
                root_el[parm]["beat_denominator"] = 2 ** (beat & 0xf)
            elif param_id == ac7paramtempo:
                length = self._read(BinaryReader.u1(self._buffer, self._pos))
                parm = 'param_tempo'
                root_el[parm]["length"] = length
                root_el[parm]["tempo"] = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
            elif param_id == ac7parammeasures:
                length = self._read(BinaryReader.u1(self._buffer, self._pos))
                parm = 'param_measures'
                root_el[parm]["length"] = length
                root_el[parm]["measures"] = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
            elif param_id == ac7paramparts:
                length = self._read(BinaryReader.u1(self._buffer, self._pos))
                parm = 'param_parts'
                root_el[parm]["length"] = length
                root_el[parm]["parts"] = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
            elif param_id == ac7paramtrackidx:
                length = self._read(BinaryReader.u1(self._buffer, self._pos))
                parm = 'param_trackidx'
                root_el[parm]["tracks"] = {}
                for j in range(int(length / 2)):
                    trackidx = self._read(BinaryReader.u1(self._buffer, self._pos))
                    trackproperty = self._read(BinaryReader.u1(self._buffer, self._pos))
                    root_el[parm]["tracks"][trackidx] = trackproperty
            elif param_id == ac7parammixeridx:
                length = self._read(BinaryReader.u1(self._buffer, self._pos))
                parm = 'param_mixeridx'
                root_el[parm]["mixer"] = {}
                for j in range(int(length / 2)):
                    trackidx = self._read(BinaryReader.u1(self._buffer, self._pos))
                    trackproperty = self._read(BinaryReader.u1(self._buffer, self._pos))
                    root_el[parm]["mixer"][trackidx] = trackproperty
            elif param_id == ac7parampartidx:
                length = self._read(BinaryReader.u1(self._buffer, self._pos))
                parm = 'param_partidx'
                root_el[parm]["parts"] = {}
                for j in range(length):
                    partid = self._read(BinaryReader.u1(self._buffer, self._pos))
                    root_el[parm]["parts"]["id"] = partid
                    partnum = partid & 0xf
                    root_el[parm]["parts"]["num"] = (partnum if partnum < 0xf else partnum - 0x10) + 1
                    scale = int((partid & 0xf0) / 0x10)
                    root_el[parm]["parts"]["scale"] = scale
                    if 7 >= scale >= 0:
                        root_el[parm]["parts"]["type"] = ac7partname[scale]
                    elif scale == 0x8:
                        root_el[parm]["parts"]["type"] = "major"
                    elif scale == 0xa:
                        root_el[parm]["parts"]["type"] = "minor"
            param_id = self._read(BinaryReader.u1(self._buffer, self._pos))
        length_zero = self._read(BinaryReader.u1(self._buffer, self._pos))
        return self._pos