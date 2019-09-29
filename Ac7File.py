import os
import struct
from BinaryReader import BinaryReader
from BinaryWriter import BinaryWriter
from Ac7Base import Ac7Base
from Ac7CommonParameters import Ac7CommonParameters
from Ac7MixerParameters import Ac7MixerParameters
from Ac7DrumParameters import Ac7DrumParameters
from Ac7OtherParameters import Ac7OtherParameters

class Ac7File(Ac7Base):
    def __init__(self):
        super().__init__()
        self.properties = {}
        self.properties['filesize'] = 0
        self.properties['common_offset'] = 0
        self.properties['mixer_offset'] = 0
        self.properties['drum_offset'] = 0
        self.properties['otherpart_offset'] = 0
        self.properties['common_parameters'] = Ac7CommonParameters()
        self.properties['mixer_parameters'] = Ac7MixerParameters()
        self.properties['drum_parameters'] = Ac7DrumParameters()
        self.properties['other_parameters'] = Ac7OtherParameters()
        self.writer = BinaryWriter()

    def _load_header(self):
        magicstr = self._read(BinaryReader.magic("AC07", "ascii", self._buffer, self._pos))
        self.properties['filesize'] = self._read(BinaryReader.u4le(self._buffer, self._pos))

    def _write_header(self, buffer):
        buffer = self.writer.str("AC07", "ascii", buffer)
        buffer = self.writer.u4le(0, buffer, "filesize") # bookmark so we can fill it in later
        return buffer

    def _load_commonoffset(self):
        self.properties['common_offset'] = self._read(BinaryReader.u4le(self._buffer, self._pos))

    def _write_commonoffset(self, buffer):
        buffer = self.writer.u4le(0, buffer, "commonoffset")
        return buffer

    def _load_mixeroffset(self):
        self.properties['mixer_offset'] = self._read(BinaryReader.u4le(self._buffer, self._pos))

    def _write_mixeroffset(self, buffer):
        buffer = self.writer.u4le(0, buffer, "mixeroffset")
        return buffer

    def _load_drumoffset(self):
        self.properties['drum_offset'] = self._read(BinaryReader.u4le(self._buffer, self._pos))

    def _write_drumoffset(self, buffer):
        buffer = self.writer.u4le(0, buffer, "drumoffset")
        return buffer

    def _load_otherpartoffset(self):
        self.properties['otherpart_offset'] = self._read(BinaryReader.u4le(self._buffer, self._pos))

    def _write_otherpartoffset(self, buffer):
        buffer = self.writer.u4le(0, buffer, "otheroffset")
        return buffer

    def _load_reservedbytes(self):
        # throw way the result
        self._read(BinaryReader.u4le(self._buffer, self._pos))

    def _write_reserved(self, buffer):
        buffer = self.writer.u4le(0xffffffff, buffer)
        return buffer

    def _load_commonmem(self):
        self._pos = self.properties['common_parameters']._load(self._buffer, self._pos,
                                                               self.properties['common_offset'])

    def _write_commonmem(self, buffer):
        buffer = self.properties['common_parameters']._write(self.writer, buffer)
        return buffer

    def _load_mixermem(self):
        self._pos = self.properties['mixer_parameters']._load(self._buffer, self._pos,
                                                               self.properties['mixer_offset'])

    def _load_drumsmem(self):
        self._pos = self.properties['drum_parameters']._load(self._buffer, self._pos,
                                                             self.properties['drum_offset'],
                                                             self.properties['otherpart_offset'])
    def _load_othermem(self):
        self._pos = self.properties['other_parameters']._load(self.properties['otherpart_offset'], self.properties['filesize'], self._buffer, self._pos)

    def load_file(self, filename):
        with open(filename, "rb") as f:
            self._pos = 0
            self._buffer = f.read()
            self._load_header()
            self._load_commonoffset()
            self._load_mixeroffset()
            self._load_drumoffset()
            self._load_otherpartoffset()
            self._load_reservedbytes()
            self._load_commonmem()
            self._load_mixermem()
            self._load_drumsmem()
            self._load_othermem()

    def write_file(self, filename, allow_overwrite=False):
        if not allow_overwrite and os.path.exists(filename):
            print("Error! I refuse to overwrite existing file {0}. Please specify a different filename.".format(filename))
            return
        with open(filename, "wb") as f:
            self._pos = 0
            buffer = bytearray()
            buffer = self._write_header(buffer)
            buffer = self._write_commonoffset(buffer)
            buffer = self._write_mixeroffset(buffer)
            buffer = self._write_drumoffset(buffer)
            buffer = self._write_otherpartoffset(buffer)
            buffer = self._write_reserved(buffer)
            buffer = self._write_commonmem(buffer)

            # fill in the bookmarks
            start_of_commonparams = self.writer.get_bookmark_position("start_of_common")
            commonparams = self.writer.get_bookmark_position("commonoffset")
            if commonparams is None or start_of_commonparams is None:
                print("Error: bookmark commonoffset/start_of_commonparams is not resolved.")
            else:
                struct.pack_into("<I", buffer, commonparams, start_of_commonparams)

            filesize_pos = self.writer.get_bookmark_position("filesize")
            struct.pack_into("<I", buffer, filesize_pos, len(buffer))
            f.write(buffer)



    def summarize(self, result):
        result.append("filesize: {0}".format(self.properties['filesize']))
        #result.append("common parameter section offset: {0}".format(self.properties['common_offset']))
        #result.append("mixer parameter section offset: {0}".format(self.properties['mixer_offset']))
        #result.append("drum parameter section offset: {0}".format(self.properties['drum_offset']))
        #result.append("other offset parameter section: {0}".format(self.properties['otherpart_offset']))
        self.properties['common_parameters']._summarize("Common parameters", result)
        self.properties['mixer_parameters']._summarize("Mixer parameters", result)
        self.properties['drum_parameters']._summarize("Drum parameters", result)
        self.properties['other_parameters']._summarize("Chord parameters", result)

        return result
