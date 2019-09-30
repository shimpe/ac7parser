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

    def write(self, format, value, buffer, bookmark=""):
        fmt = {
            "u1" : "B", "s1" : "b", "u2le" : "<H", "s2le" : "<h",
            "u4le" : "<I", "s4le" : "<i", "u8le": "<Q", "s8le" : "<q",
            "f2le" : "<e", "f4le" : "<f", "f8le" : "<d",
            "u2be": ">H", "s2be": ">h",
            "u4be": ">I", "s4be": ">i", "u8be": ">Q", "s8be": ">q",
            "f2be": ">e", "f4be": ">f", "f8be": ">d"
        }
        self.set_bookmark(bookmark, len(buffer))
        buffer = buffer + struct.pack(fmt[format], value)
        return buffer

    def udynle(self, size, value, buffer, bookmark=""):
        lookup = {
            1 : "u1",
            2 : "u2le",
            4 : "u4le",
            8 : "u8le",
        }
        return self.write(lookup[size], value, buffer, bookmark)

    def sdynle(self, size, value, buffer, bookmark=""):
        lookup = {
            1: "s1",
            2: "s2le",
            4: "s4le",
            8: "s8le",
        }
        return self.write(lookup[size], value, buffer, bookmark)

    def fdynle(self, size, value, buffer, bookmark=""):
        lookup = {
            2: "f2le",
            4: "f4le",
            8: "f8le",
        }
        return self.write(lookup[size], value, buffer, bookmark)

    def udynbe(self, size, value, buffer, bookmark=""):
        lookup = {
            1 : "u1",
            2 : "u2be",
            4 : "u4be",
            8 : "u8be",
        }
        return self.write(lookup[size], value, buffer, bookmark)

    def sdynbe(self, size, value, buffer, bookmark=""):
        lookup = {
            1: "s1",
            2: "s2be",
            4: "s4be",
            8: "s8be",
        }
        return self.write(lookup[size], value, buffer, bookmark)

    def fdynbe(self, size, value, buffer, bookmark=""):
        lookup = {
            2: "f2be",
            4: "f4be",
            8: "f8be",
        }
        return self.write(lookup[size], value, buffer, bookmark)

    def str(self, value, encoding, buffer, bookmark=""):
        self.set_bookmark(bookmark, len(buffer))
        formatstr = "{0}s".format(len(value))
        buffer = buffer + struct.pack(formatstr, value.encode(encoding))
        return buffer
