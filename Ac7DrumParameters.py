from collections import defaultdict
from BinaryReader import BinaryReader
from Ac7Base import Ac7Base

class Ac7DrumParameters(Ac7Base):
    def __init__(self):
        super().__init__()
        self.properties = {
            'track_offsets' : [],
            'track_descriptors' : defaultdict(lambda : {})
        }

    def _load(self, buffer, pos, drum_offset, otherpart_offset):
        self._buffer = buffer
        self._pos = pos
        self.properties['drum_offset'] = drum_offset
        if (self._pos != drum_offset):
            print ("Warning... expected to be at drum offset, but something went wrong.\nPlease submit a bug report on github and attach your .ac7 file.\nself._pos = {0}, drum_offset = {1}".format(self._pos, drum_offset))
        self._pos = drum_offset
        magic = self._read(BinaryReader.magic("DRUM", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.u4le(self._buffer, self._pos))
        trackcount = self._read(BinaryReader.u2le(self._buffer, self._pos))
        for i in range(trackcount):
            self.properties['track_offsets'].append(self._read(BinaryReader.u4le(self._buffer, self._pos)))
        for i in range(trackcount):
            self.properties['track_descriptors'][i]['casioevents'] = []
            offset = self.properties['track_offsets'][i]
            if i == trackcount - 1:
                next_offset = otherpart_offset
            else:
                next_offset = self.properties['track_offsets'][i+1]
            for j in range(int((next_offset - offset)/3)):
                casioevent = {}
                casioevent['delta'] = self._read(BinaryReader.u1(self._buffer, self._pos))
                casioevent['note_or_event'] = self._read(BinaryReader.u1(self._buffer, self._pos))
                casioevent['vel_or_val'] = self._read(BinaryReader.u1(self._buffer, self._pos))
                self.properties['track_descriptors'][i]['casioevents'].append(casioevent)
        #print(self.properties)
        return self._pos

    def _summarize(self, title, result):
        result.append(title)
        result.append("*"*len(title))
        result.append("Number of tracks: {0}".format(len(self.properties['track_descriptors'])))
        for i in range(len(self.properties['track_descriptors'])):
            tracktitle = "  track {0}".format(i)
            result.append(tracktitle)
            result.append("  " + "-"*(len(tracktitle)-2))
            result.append(self.properties['track_descriptors'][i]['casioevents'].__repr__().replace("}, ", "},\n"))
        return result