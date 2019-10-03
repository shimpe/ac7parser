from collections import defaultdict
from BinaryReader import BinaryReader
from Ac7Base import Ac7Base

class Ac7MixerParameters(Ac7Base):
    def __init__(self):
        super().__init__()
        self.properties = {'mixer_offset': 0, 'parameter_offsets' : [], 'parameters' : defaultdict(lambda:{})}

    def _load(self, buffer, pos, mixer_offset):
        self._buffer = buffer
        self._pos = pos
        self.properties['mixer_offset'] = mixer_offset
        if self._pos != mixer_offset:
            raise Exception("Warning... expected to be at mixer offset, but something went wrong.\nPlease submit a bug report on github and attach your .ac7 file.\n self._pos = {0}, mixer_offset = {1}").format(self._pos, mixer_offset)
        self._pos = mixer_offset
        magic = self._read(BinaryReader.magic("MIXR", "ascii", self._buffer, self._pos))
        size = self._read(BinaryReader.read("u4le", self._buffer, self._pos))
        paramcount = self._read(BinaryReader.read("u2le", self._buffer, self._pos))
        for i in range(paramcount):
            self.properties['parameter_offsets'].append(self._read(BinaryReader.read("u4le", self._buffer, self._pos)))
        for i in range(paramcount):
            self.properties['parameters'][i]['tone'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['parameters'][i]['bank'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['parameters'][i]['volume'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['parameters'][i]['pan'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['parameters'][i]['reverb'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))
            self.properties['parameters'][i]['chorus'] = self._read(BinaryReader.read("u1", self._buffer, self._pos))

        #print(self.properties)
        return self._pos

    def _write(self, writer, buffer):
        buffer = writer.str("MIXR", "ascii", buffer, "start_of_mixerparam")
        buffer = writer.write("u4le", 0, buffer, "mixer_size")
        paramcount = len(self.properties['parameters'])
        buffer = writer.write("u2le", paramcount, buffer, "start_of_mixersize")
        for i in range(paramcount):
            buffer = writer.write("u4le", self.properties['parameter_offsets'][i], buffer)
        for i in range(paramcount):
            buffer = writer.write("u1", self.properties['parameters'][i]['tone'], buffer)
            buffer = writer.write("u1", self.properties['parameters'][i]['bank'], buffer)
            buffer = writer.write("u1", self.properties['parameters'][i]['volume'], buffer)
            buffer = writer.write("u1", self.properties['parameters'][i]['pan'], buffer)
            buffer = writer.write("u1", self.properties['parameters'][i]['reverb'], buffer)
            buffer = writer.write("u1", self.properties['parameters'][i]['chorus'], buffer)

        mixersize = len(buffer) - writer.get_bookmark_position("start_of_mixersize")
        buffer = writer.write_into("mixer_size", mixersize, buffer)
        return buffer

    def _summarize(self, title, result):
        result.append(title)
        result.append("*"*len(title))
        result.append("Number of parameters: {0}".format(len(self.properties['parameters'])))
        for i in range(len(self.properties['parameters'])):
            result.append(self.properties['parameters'][i].__repr__())

        return result