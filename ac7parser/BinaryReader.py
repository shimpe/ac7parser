import struct


class BinaryReader(object):
    def __init__(self):
        pass

    @staticmethod
    def read(formaat, buffer, pos):
        format_to_structfmt = {
            "u1"  : "B", "s1": "b", "u2le": "<H", "s2le": "<h",
            "u4le": "<I", "s4le": "<i", "u8le": "<Q", "s8le": "<q",
            "f2le": "<e", "f4le": "<f", "f8le": "<d",
            "u2be": ">H", "s2be": ">h", "u4be": ">I",
            "s4be": ">i", "u8be": ">Q", "s8be": ">q",
            "f2be": ">e", "f4be": ">f", "f8be": ">d"
        }
        fmt = format_to_structfmt[formaat]
        fmt_cs = fmt[-1]
        value = struct.unpack_from(fmt, buffer[pos:], 0)[0]
        return value, pos + struct.calcsize(fmt_cs)

    @staticmethod
    def udynle(size, buffer, pos):
        lookup = {
            1: "u1",
            2: "u2le",
            4: "u4le",
            8: "u8le",
        }
        return BinaryReader.read(lookup[size], buffer, pos)

    @staticmethod
    def sdynle(size, buffer, pos):
        lookup = {
            1: "s1",
            2: "s2le",
            4: "s4le",
            8: "s8le",
        }
        return BinaryReader.read(lookup[size], buffer, pos)

    @staticmethod
    def fdynle(size, buffer, pos):
        lookup = {
            2: "f2le",
            4: "f4le",
            8: "f8le",
        }
        return BinaryReader.read(lookup[size], buffer, pos)

    @staticmethod
    def udynbe(size, buffer, pos):
        lookup = {
            1: "u1",
            2: "u2be",
            4: "u4be",
            8: "u8be",
        }
        return BinaryReader.read(lookup[size], buffer, pos)

    @staticmethod
    def sdynbe(size, buffer, pos):
        lookup = {
            1: "s1",
            2: "s2be",
            4: "s4be",
            8: "s8be",
        }
        return BinaryReader.read(lookup[size], buffer, pos)

    @staticmethod
    def fdynbe(size, buffer, pos):
        lookup = {
            2: "f2be",
            4: "f4be",
            8: "f8be",
        }
        return BinaryReader.read(lookup[size], buffer, pos)

    @staticmethod
    def str(length, encoding, buffer, pos):
        formatstr = "{0}s".format(length)
        value = struct.unpack_from(formatstr, buffer[pos:], 0)[0].decode(encoding)
        return value, pos + struct.calcsize(formatstr)

    @staticmethod
    def magic(expected, encoding, buffer, pos):
        formatstr = "{0}s".format(len(expected))
        if encoding is not None:
            value = struct.unpack_from(formatstr, buffer[pos:], 0)[0].decode(encoding)
        else:
            value = struct.unpack_from(formatstr, buffer[pos:], 0)[0]
        if value != expected:
            assert False, "Expected MAGIC not found. File format error."
        return value, pos + struct.calcsize(formatstr)
