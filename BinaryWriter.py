import struct

class BinaryWriter(object):
    def __init__(self):
        self.bookmarks = {}

    def get_bookmark_position(self, bookmark):
        if bookmark in self.bookmarks:
            return self.bookmarks[bookmark]
        return None

    def set_bookmark(self, bookmark, position):
        if bookmark:
            if bookmark in self.bookmarks:
                print("Warning: overwriting existing bookmark {0}. This may cause trouble later.".format(bookmark))
            self.bookmarks[bookmark] = position

    def u1(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("B", value)
        return buffer

    def s1(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("b", value)
        return buffer

    def u2le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<H", value)
        return buffer

    def s2le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<h", value)
        return buffer

    def u4le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<I", value)
        return buffer

    def s4le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<i", value)
        return buffer

    def u8le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<Q", value)
        return buffer

    def s8le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<q", value)
        return buffer

    def f2le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<e", value)
        return buffer

    def f4le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("f", value)
        return buffer

    def f8le(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack("<d", value)
        return buffer

    def udynle(self, size, value, buffer, bookmark=""):
        lookup = {
            1 : self.u1,
            2 : self.u2le,
            4 : self.u4le,
            8 : self.u8le,
        }
        return lookup[size](value, buffer, bookmark)

    def sdynle(self, size, value, buffer, bookmark=""):
        lookup = {
            1: self.s1,
            2: self.s2le,
            4: self.s4le,
            8: self.s8le,
        }
        return lookup[size](value, buffer, bookmark)

    def fdynle(self, size, value, buffer, bookmark=""):
        lookup = {
            2: self.f2le,
            4: self.f4le,
            8: self.f8le,
        }
        return lookup[size](value, buffer, bookmark)

    def u2be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(">H", value)
        return buffer

    def s2be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(">h", value)
        return buffer

    def u4be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(">I", value)
        return buffer

    def s4be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(">i", value)
        return buffer

    def u8be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(">Q", value)
        return buffer

    def s8be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(">q", value)
        return buffer

    def f2be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(">e", value)
        return buffer

    def udynbe(self, size, value, buffer, bookmark=""):
        lookup = {
            1 : self.u1,
            2 : self.u2be,
            4 : self.u4be,
            8 : self.u8be,
        }
        return lookup[size](value, buffer, bookmark)

    def sdynbe(self, size, value, buffer, bookmark=""):
        lookup = {
            1: self.s1,
            2: self.s2be,
            4: self.s4be,
            8: self.s8be,
        }
        return lookup[size](value, buffer, bookmark)

    def fdynbe(self, size, value, buffer, bookmark=""):
        lookup = {
            2: self.f2be,
            4: self.f4be,
            8: self.f8be,
        }
        return lookup[size](value, buffer, bookmark)

    def f4be(self, size, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pact(">f", value)
        return buffer

    def f8be(self, value, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pact(">d", value)
        return buffer

    def str(self, value, encoding, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        formatstr = "{0}s".format(len(value))
        buffer = buffer + struct.pack(formatstr, value.encode(encoding))
        return buffer
