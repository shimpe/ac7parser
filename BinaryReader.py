import struct

class BinaryReader(object):
    def __init__(self):
        pass

    @staticmethod
    def u1(buffer, pos):
        value = struct.unpack_from("B", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("B")

    @staticmethod
    def s1(buffer, pos):
        value = struct.unpack_from("b", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("b")

    @staticmethod
    def u2le(buffer, pos):
        value = struct.unpack_from("<H", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("H")

    @staticmethod
    def s2le(buffer, pos):
        value = struct.unpack_from("<h", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("h")

    @staticmethod
    def u4le(buffer, pos):
        value = struct.unpack_from("<I", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("I")

    @staticmethod
    def s4le(buffer, pos):
        value = struct.unpack_from("<i", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("i")

    @staticmethod
    def u8le(buffer, pos):
        value = struct.unpack_from("<Q", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("Q")

    @staticmethod
    def s8le(buffer, pos):
        value = struct.unpack_from("<q", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("q")

    @staticmethod
    def f2le(buffer, pos):
        value = struct.unpack_from("<e", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("e")

    @staticmethod
    def f4le(buffer, pos):
        value = struct.unpack_from("<f", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("f")

    @staticmethod
    def f8le(buffer, pos):
        value = struct.unpack_from("<d", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("d")

    @staticmethod
    def udynle(size, buffer, pos):
        lookup = {
            1 : BinaryReader.u1,
            2 : BinaryReader.u2le,
            4 : BinaryReader.u4le,
            8 : BinaryReader.u8le,
        }
        return lookup[size](buffer, pos)

    @staticmethod
    def sdynle(size, buffer, pos):
        lookup = {
            1: BinaryReader.s1,
            2: BinaryReader.s2le,
            4: BinaryReader.s4le,
            8: BinaryReader.s8le,
        }
        return lookup[size](buffer, pos)

    @staticmethod
    def fdynle(size, buffer, pos):
        lookup = {
            2: BinaryReader.f2le,
            4: BinaryReader.f4le,
            8: BinaryReader.f8le,
        }
        return lookup[size](buffer, pos)

    @staticmethod
    def u2be(buffer, pos):
        value = struct.unpack_from(">H", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("H")

    @staticmethod
    def s2be(buffer, pos):
        value = struct.unpack_from(">h", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("h")

    @staticmethod
    def u4be(buffer, pos):
        value = struct.unpack_from(">I", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("I")

    @staticmethod
    def s4be(buffer, pos):
        value = struct.unpack_from(">i", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("i")

    @staticmethod
    def u8be(buffer, pos):
        value = struct.unpack_from(">Q", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("Q")

    @staticmethod
    def s8be(buffer, pos):
        value = struct.unpack_from(">q", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("q")

    @staticmethod
    def f2be(buffer, pos):
        value = struct.unpack_from(">e", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("e")

    @staticmethod
    def udynbe(size, buffer, pos):
        lookup = {
            1 : BinaryReader.u1,
            2 : BinaryReader.u2be,
            4 : BinaryReader.u4be,
            8 : BinaryReader.u8be,
        }
        return lookup[size](buffer, pos)

    @staticmethod
    def sdynbe(size, buffer, pos):
        lookup = {
            1: BinaryReader.s1,
            2: BinaryReader.s2be,
            4: BinaryReader.s4be,
            8: BinaryReader.s8be,
        }
        return lookup[size](buffer, pos)

    @staticmethod
    def fdynbe(size, buffer, pos):
        lookup = {
            2: BinaryReader.f2be,
            4: BinaryReader.f4be,
            8: BinaryReader.f8be,
        }
        return lookup[size](buffer, pos)

    @staticmethod
    def f4be(buffer, pos):
        value = struct.unpack_from(">f", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("f")

    @staticmethod
    def f8be(buffer, pos):
        value = struct.unpack_from(">d", buffer[pos:], 0)[0]
        return value, pos+struct.calcsize("d")

    @staticmethod
    def str(length, encoding, buffer, pos):
        formatstr = "{0}s".format(length)
        value = struct.unpack_from(formatstr, buffer[pos:], 0)[0].decode(encoding)
        return value, pos+struct.calcsize(formatstr)

    @staticmethod
    def magic(expected, encoding, buffer, pos):
        formatstr = "{0}s".format(len(expected))
        if encoding is not None:
            value = struct.unpack_from(formatstr, buffer[pos:], 0)[0].decode(encoding)
        else:
            value = struct.unpack_from(formatstr, buffer[pos:], 0)[0]
        if value != expected:
            assert False, "Expected MAGIC not found. File format error."
        return value, pos+struct.calcsize(formatstr)
