from collections import defaultdict
from Ac7Base import Ac7Base
from BinaryReader import BinaryReader

class Ac7OtherParameters(Ac7Base):
    def __init__(self):
        self._buffer = None
        self.pos = 0
        self.properties = {'otherpart_offset' : 0,
                           'track_descriptors': defaultdict(lambda: {}),
                           'filesize' : 0
                           }

    def _load(self, otherpart_offset, filesize, buffer, pos):
        self._buffer = buffer
        self._pos = pos
        self.properties['filesize'] = filesize
        self.properties['otherpart_offset'] = otherpart_offset
        if self._pos != otherpart_offset:
            raise Exception(
                "Warning... expected to be at 'other' parameters offset, but something went wrong.\nPlease submit a bug report on github and attach your .ac7 file.\n self._pos = {0}, otherpart_offset = {1}.").format(
                self._pos, otherpart_offset)
        self._pos = otherpart_offset
        magic = self._read(BinaryReader.magic("OTHR", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.u4le(self._buffer, self._pos))
        trackcount = self._read(BinaryReader.u2le(self._buffer, self._pos))
        self.properties['track_offsets'] = {}
        for i in range(trackcount):
            self.properties['track_offsets'][i] = self._read(BinaryReader.u4le(self._buffer, self._pos))
        for i in range(trackcount):
            self.properties['track_descriptors'][i]['chordtable'] = self._read(BinaryReader.u1(self._buffer, self._pos))
            self.properties['track_descriptors'][i]['chordparam'] = self._read(BinaryReader.u1(self._buffer, self._pos))
            self.properties['track_descriptors'][i]['roothelper'] = self._read(BinaryReader.u1(self._buffer, self._pos))
            self.properties['track_descriptors'][i]['froot'] = int(self.properties['track_descriptors'][i]['roothelper']) >> 3
            self.properties['track_descriptors'][i]['break'] = self.properties['track_descriptors'][i]['chordparam']  >> 4
            self.properties['track_descriptors'][i]['inversion'] = int((self.properties['track_descriptors'][i]['chordparam'] - self.properties['track_descriptors'][i]['break'] * 0x10) / 4)
            self.properties['track_descriptors'][i]['retrigger'] = self.properties['track_descriptors'][i]['chordparam'] - self.properties['track_descriptors'][i]['break'] * 0x10 - self.properties['track_descriptors'][i]['inversion'] * 4
            self.properties['track_descriptors'][i]['casioevents'] = []
            offset = self.properties['track_offsets'][i]
            next_offset = filesize if i == trackcount-1 else self.properties['track_offsets'][i+1]
            if self._pos != offset + 3:
               print("i = {0}, j = {1} unexpected offset. Please file a bug report on github and attach your .ac7 file. Self-correcting offset and continuing.")
            self._pos = offset + 3
            no_of_events_float = (next_offset - offset - 3)/3
            no_of_events = int(no_of_events_float)
            for j in range(no_of_events):
                casioevent = {}
                casioevent['delta'] = self._read(BinaryReader.u1(self._buffer, self._pos))
                casioevent['note'] = self._read(BinaryReader.u1(self._buffer, self._pos))
                casioevent['velocity'] = self._read(BinaryReader.u1(self._buffer, self._pos))
                self.properties['track_descriptors'][i]['casioevents'].append(casioevent)

        print(self.properties)