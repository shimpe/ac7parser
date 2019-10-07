from collections import defaultdict

from .Ac7Base import Ac7Base
from .Ac7CasioEventAnalyzer import Ac7CasioEventAnalyzer
from .BinaryReader import BinaryReader


class Ac7DrumParameters(Ac7Base):
    def __init__(self):
        super().__init__()
        self.properties = {
            'track_offsets'    : [],
            'track_descriptors': defaultdict(lambda: {})
        }
        self.analyzer = Ac7CasioEventAnalyzer()

    def _load(self, buffer, pos, drum_offset, otherpart_offset):
        self._buffer = buffer
        self._pos = pos
        self.properties['drum_offset'] = drum_offset
        if (self._pos != drum_offset):
            print(
                "Warning... expected to be at drum offset, but something went wrong.\nPlease submit a bug report on github and attach your .ac7 file.\nself._pos = {0}, drum_offset = {1}".format(
                    self._pos, drum_offset))
        self._pos = drum_offset
        magic = self._read(BinaryReader.magic("DRUM", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.read("u4le", self._buffer, self._pos))
        trackcount = self._read(BinaryReader.read("u2le", self._buffer, self._pos))
        for i in range(trackcount):
            self.properties['track_offsets'].append(self._read(BinaryReader.read("u4le", self._buffer, self._pos)))
        for i in range(trackcount):
            self.properties['track_descriptors'][i]['casioevents'] = []
            offset = self.properties['track_offsets'][i]
            if i == trackcount - 1:
                next_offset = otherpart_offset
            else:
                next_offset = self.properties['track_offsets'][i + 1]
            for j in range(int((next_offset - offset) / 3)):
                casioevent = {}
                casioevent['delta'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                casioevent['note_or_event'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                casioevent['vel_or_val'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
                self.analyzer._annotate(casioevent)
                self.properties['track_descriptors'][i]['casioevents'].append(casioevent)
        # print(self.properties)
        return self._pos

    def _write(self, writer, buffer):
        buffer = writer.str("DRUM", "ascii", buffer, "start_of_drumsparam")
        buffer = writer.write("u4le", 0, buffer, "size_of_drumsparam")
        trackcount = len(self.properties['track_descriptors'])
        buffer = writer.write("u2le", trackcount, buffer)
        for i in range(trackcount):
            buffer = writer.write("u4le", 0, buffer, "drum_track_offset{0}".format(i))
        for i in range(trackcount):
            for l in range(len(self.properties['track_descriptors'][i]['casioevents'])):
                buffer = writer.write("u1", self.properties['track_descriptors'][i]['casioevents'][l]['delta'], buffer,
                                      "start_of_drum_track{0}".format(i) if l == 0 else "")
                buffer = writer.write("u1", self.properties['track_descriptors'][i]['casioevents'][l]['note_or_event'],
                                      buffer)
                buffer = writer.write("u1", self.properties['track_descriptors'][i]['casioevents'][l]['vel_or_val'],
                                      buffer)
        # fill in bookmarks
        for i in range(trackcount):
            value = writer.get_bookmark_position("start_of_drum_track{0}".format(i))
            buffer = writer.write_into("drum_track_offset{0}".format(i), value, buffer)

        buffer = writer.write_into("size_of_drumsparam",
                                   len(buffer) - writer.get_bookmark_position("start_of_drumsparam"),
                                   buffer)
        return buffer

    def _summarize(self, title, result):
        result.append(title)
        result.append("*" * len(title))
        result.append("Number of tracks: {0}".format(len(self.properties['track_descriptors'])))
        for i in range(len(self.properties['track_descriptors'])):
            tracktitle = "  track {0}".format(i + 1)
            result.append(tracktitle)
            result.append("  " + "-" * (len(tracktitle) - 2))
            result.append(self.properties['track_descriptors'][i]['casioevents'].__repr__().replace("}, ", "},\n"))
        return result
