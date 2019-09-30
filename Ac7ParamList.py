from BinaryReader import BinaryReader
from Ac7Base import Ac7Base
from Ac7Constants import *
from math import log2

class Ac7ParamList(Ac7Base):
    def __init__(self):
        self._buffer = None
        self._pos = 0
        self.i2s = { ac7paramnomore : "param_nomore",
                     ac7parambeat: "param_beat",
                     ac7paramtempo: "param_tempo",
                     ac7parammeasures : "param_measures",
                     ac7paramparts : "param_parts",
                     ac7paramtrackidx : "param_trackidx",
                     ac7parammixeridx : "param_mixeridx",
                     ac7parampartidx : "param_partidx"}
        self.s2i = { "param_nomore" : ac7paramnomore ,
                     "param_beat" : ac7parambeat,
                     "param_tempo" : ac7paramtempo,
                     "param_measures" : ac7parammeasures,
                     "param_parts" : ac7paramparts ,
                     "param_trackidx" : ac7paramtrackidx,
                     "param_mixeridx" : ac7parammixeridx ,
                     "param_partidx" : ac7parampartidx}

    def _load_parameter_list(self, root_el, buffer, pos):
        self._buffer = buffer
        self._pos = pos
        param_id = self._read(BinaryReader.read("u1", self._buffer, self._pos))
        while param_id != ac7paramnomore:
            parm = self.i2s[param_id]
            if param_id == ac7parambeat:
                length = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                root_el[parm]["length"] = length
                beat = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
                root_el[parm]["beat_nominator"] = beat >> 4
                root_el[parm]["beat_denominator"] = 2 ** (beat & 0xf)
            elif param_id == ac7paramtempo:
                length = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                root_el[parm]["length"] = length
                root_el[parm]["tempo"] = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
            elif param_id == ac7parammeasures:
                length = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                root_el[parm]["length"] = length
                root_el[parm]["measures"] = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
            elif param_id == ac7paramparts:
                length = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                root_el[parm]["length"] = length
                root_el[parm]["parts"] = self._read(BinaryReader.udynle(length, self._buffer, self._pos))
            elif param_id == ac7paramtrackidx:
                length = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                root_el[parm]["tracks"] = {}
                for j in range(int(length / 2)):
                    trackidx = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                    trackproperty = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                    root_el[parm]["tracks"][trackidx] = trackproperty
            elif param_id == ac7parammixeridx:
                length = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                root_el[parm]["mixer"] = {}
                for j in range(int(length / 2)):
                    trackidx = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                    trackproperty = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                    root_el[parm]["mixer"][trackidx] = trackproperty
            elif param_id == ac7parampartidx:
                length = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                root_el[parm]["parts"] = {}
                for j in range(length):
                    root_el[parm]["parts"][j] = {}
                    partid = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                    root_el[parm]["parts"][j]["id"] = partid
                    partnum = partid & 0xf
                    root_el[parm]["parts"][j]["num"] = (partnum if partnum < 0xf else partnum - 0x10) + 1
                    scale = int((partid & 0xf0) >> 4)
                    root_el[parm]["parts"][j]["scale"] = scale
                    if 7 >= scale >= 0:
                        root_el[parm]["parts"][j]["type"] = ac7partname[scale]
                    elif scale == 0x8:
                        root_el[parm]["parts"][j]["type"] = "major"
                    elif scale == 0xa:
                        root_el[parm]["parts"][j]["type"] = "minor"
            param_id = self._read(BinaryReader.read("u1", self._buffer, self._pos))
        length_zero = self._read(BinaryReader.read("u1", self._buffer, self._pos))
        return self._pos

    def _write_parameter_list(self, root_el, writer, buffer):
        for parm in root_el:
            param_id = self.s2i[parm]
            buffer = writer.write("u1", param_id, buffer)
            if param_id == ac7parambeat:
                length = root_el[parm]["length"]
                buffer = writer.write("u1", length, buffer)
                beat = (root_el[parm]["beat_nominator"] << 4) | int(log2(root_el[parm]["beat_denominator"]))
                buffer = writer.udynle(length, beat, buffer)
            elif param_id == ac7paramtempo:
                length = root_el[parm]["length"]
                buffer = writer.write("u1", length, buffer)
                tempo = root_el[parm]["tempo"]
                buffer = writer.udynle(length, tempo, buffer)
            elif param_id == ac7parammeasures:
                length = root_el[parm]["length"]
                buffer = writer.write("u1", length, buffer)
                measures = root_el[parm]["measures"]
                buffer = writer.udynle(length, measures, buffer)
            elif param_id == ac7paramparts:
                length = root_el[parm]["length"]
                buffer = writer.write("u1", length, buffer)
                parts = root_el[parm]["parts"]
                buffer = writer.udynle(length, parts, buffer)
            elif param_id == ac7paramtrackidx:
                length = len(root_el[parm]["tracks"])*2
                buffer = writer.write("u1", length, buffer)
                for trackidx in root_el[parm]["tracks"]:
                    buffer = writer.write("u1", trackidx, buffer)
                    buffer = writer.write("u1", root_el[parm]["tracks"][trackidx], buffer)
            elif param_id == ac7parammixeridx:
                length = len(root_el[parm]["mixer"])*2
                buffer = writer.write("u1", length, buffer)
                for trackidx in root_el[parm]["mixer"]:
                    buffer = writer.write("u1", trackidx, buffer)
                    buffer = writer.write("u1", root_el[parm]["mixer"][trackidx], buffer)
            elif param_id == ac7parampartidx:
                length = len(root_el[parm]["parts"])
                buffer = writer.write("u1", length, buffer)
                for j in range(length):
                    scale = ac7partid[root_el[parm]["parts"][j]["type"]]
                    num = root_el[parm]["parts"][j]["num"]
                    partno =  num-1 if num != 0 else 0xf
                    total = (num << 4) | partno
                    buffer = writer.write("u1", total, buffer)
        buffer = writer.write("u1", ac7paramnomore, buffer)
        buffer = writer.write("u1", 0, buffer)
        return buffer