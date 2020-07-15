from collections import defaultdict

from .Ac7Base import Ac7Base
from .Ac7CasioEventAnalyzer import Ac7CasioEventAnalyzer
from .Ac7TrackLockRemover import Ac7TrackLockRemover
from .BinaryReader import BinaryReader


class Ac7OtherParameters(Ac7Base):
    def __init__(self):
        super().__init__()
        self._buffer = None
        self.pos = 0
        self.properties = {'otherpart_offset' : 0,
                           'track_descriptors': defaultdict(lambda: {}),
                           'filesize'         : 0
                           }
        self.analyzer = Ac7CasioEventAnalyzer()

    def _load(self, otherpart_offset, filesize, buffer, pos):
        self._buffer = buffer
        self._pos = pos
        self.properties['filesize'] = filesize
        self.properties['otherpart_offset'] = otherpart_offset
        if self._pos != otherpart_offset:
            raise Exception(
                "Warning... expected to be at 'other' parameters offset, but something went wrong.\nPlease submit a bug report on github and attach your .ac7 file.\n self._pos = {0}, otherpart_offset = {1}.".format(
                self._pos, otherpart_offset))
        self._pos = otherpart_offset
        magic = self._read(BinaryReader.magic("OTHR", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.read("u4le", self._buffer, self._pos))
        trackcount = self._read(BinaryReader.read("u2le", self._buffer, self._pos))
        self.properties['track_offsets'] = {}
        for i in range(trackcount):
            self.properties['track_offsets'][i] = self._read(BinaryReader.read("u4le", self._buffer, self._pos))
        for i in range(trackcount):
            self.properties['track_descriptors'][i]['chordtable'] = self._read(
                BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['track_descriptors'][i]['chordtable_interpretation'] = self.chordtable_to_name(
                self.properties['track_descriptors'][i]['chordtable'])
            self.properties['track_descriptors'][i]['chordparam'] = self._read(
                BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['track_descriptors'][i]['roothelper'] = self._read(
                BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['track_descriptors'][i]['froot'] = int(
                self.properties['track_descriptors'][i]['roothelper']) >> 3
            self.properties['track_descriptors'][i]['break'] = self.properties['track_descriptors'][i][
                                                                   'chordparam'] >> 4
            self.properties['track_descriptors'][i]['inversion'] = int(
                self.properties['track_descriptors'][i]['chordparam'] & 0xf)
            self.properties['track_descriptors'][i]['retrigger'] = self.properties['track_descriptors'][i][
                                                                       'chordparam'] - \
                                                                   self.properties['track_descriptors'][i][
                                                                       'break'] * 0x10 - \
                                                                   self.properties['track_descriptors'][i][
                                                                       'inversion'] * 4
            self.properties['track_descriptors'][i]['casioevents'] = []
            offset = self.properties['track_offsets'][i]
            next_offset = filesize if i == trackcount - 1 else self.properties['track_offsets'][i + 1]
            if self._pos != offset + 3:
                print(
                    "i = {0}, j = {1} unexpected offset. Please file a bug report on github and attach your .ac7 file. Self-correcting offset and continuing.")
            self._pos = offset + 3
            no_of_events_float = (next_offset - offset - 3) / 3
            no_of_events = int(no_of_events_float)
            for j in range(no_of_events):
                casioevent = {'delta'        : self._read(BinaryReader.read("u1", self._buffer, self._pos)),
                              'note_or_event': self._read(BinaryReader.read("u1", self._buffer, self._pos)),
                              'vel_or_val'   : self._read(BinaryReader.read("u1", self._buffer, self._pos))}
                self.analyzer._annotate(casioevent)
                self.properties['track_descriptors'][i]['casioevents'].append(casioevent)

    def _write(self, writer, buffer):
        buffer = writer.str("OTHR", "ascii", buffer, "start_of_otherparams")
        buffer = writer.write("u4le", 0, buffer, "otherparam_size")
        trackcount = len(self.properties['track_descriptors'])
        buffer = writer.write("u2le", trackcount, buffer)
        for i in range(trackcount):
            buffer = writer.write("u4le", 0, buffer, "other_offset{0}".format(i))
        for i in range(trackcount):
            buffer = writer.write("u1", self.properties['track_descriptors'][i]['chordtable'], buffer,
                                  "start_of_otheroffset{0}".format(i))
            buffer = writer.write("u1", self.properties['track_descriptors'][i]['chordparam'], buffer)
            buffer = writer.write("u1", self.properties['track_descriptors'][i]['roothelper'], buffer)

            # experimental track unlock
            tlr = Ac7TrackLockRemover()
            self.properties['track_descriptors'][i]['casioevents'] = tlr.remove_lock(self.properties['track_descriptors'][i]['casioevents'])

            casioevents = self.properties['track_descriptors'][i]['casioevents']
            no_of_events = len(casioevents)
            for j in range(no_of_events):
                buffer = writer.write("u1", casioevents[j]['delta'], buffer)
                buffer = writer.write("u1", casioevents[j]['note_or_event'], buffer)
                buffer = writer.write("u1", casioevents[j]['vel_or_val'], buffer)

        # fill in bookmarks
        for i in range(trackcount):
            value = writer.get_bookmark_position("start_of_otheroffset{0}".format(i))
            buffer = writer.write_into("other_offset{0}".format(i), value, buffer)
        buffer = writer.write_into("otherparam_size",
                                   len(buffer) - writer.get_bookmark_position("start_of_otherparams"),
                                   buffer)
        return buffer

    def chordtable_to_name(self, chordtable):
        table = {
            0 : "bass",
            1 : "bass 7th",
            2 : "chord",
            3 : "chord var2",
            4 : "chord var3",
            5 : "chord var4",
            6 : "chord 7th",
            7 : "chord minor",
            8 : "chord phrase major",
            9 : "chord phrase minor",
            10: "chord phrase penta",
            11: "intro natural minor",
            12: "intro melodic minor",
            13: "intro harmonic minor",
            14: "intro no-change",
            15: "intro dorian"
        }
        if chordtable not in table:
            print("Unknown chord table entry {0}. Please file a bug report on github and attach your .ac7 file.".format(
                chordtable))
            return "UNKNOWN chord table {0}".format(chordtable)
        return table[chordtable]

    def _summarize(self, title, result):
        result.append(title)
        result.append("*" * len(title))
        for i in range(len(self.properties['track_descriptors'])):
            tracktitle = "  track {0}".format(i + 1)
            result.append(tracktitle)
            result.append("  " + "-" * (len(tracktitle) - 2))
            result.append("  chord conversion table: {0}".format(
                self.properties['track_descriptors'][i]['chordtable_interpretation']))
            result.append("  force root: {0}".format(self.properties['track_descriptors'][i]['froot']))
            result.append("  break: {0}".format(self.properties['track_descriptors'][i]['break']))
            result.append("  inversion: {0}".format(self.properties['track_descriptors'][i]['inversion']))
            result.append("  retrigger: {0}".format(self.properties['track_descriptors'][i]['retrigger']))
            result.append("  notes: {0}".format(
                self.properties['track_descriptors'][i]['casioevents'].__repr__().replace("}, ", "},\n")))
        return result
