import struct

class BinaryWriter(object):
    def __init__(self):
        self.bookmarks = {}
        self.unresolved = set()

    def get_bookmark_position(self, bookmark):
        if bookmark in self.bookmarks:
            return self.bookmarks[bookmark][0]
        else:
            print("Warning: trying to look up non-existing bookmark {0} in {1}".format(bookmark, self.bookmarks))
        return None

    def get_bookmark_fmt(self, bookmark):
        if bookmark in self.bookmarks:
            fmt = {
                "u1"  : "B", "s1": "b", "u2le": "<H", "s2le": "<h",
                "u4le": "<I", "s4le": "<i", "u8le": "<Q", "s8le": "<q",
                "f2le": "<e", "f4le": "<f", "f8le": "<d",
                "u2be": ">H", "s2be": ">h",
                "u4be": ">I", "s4be": ">i", "u8be": ">Q", "s8be": ">q",
                "f2be": ">e", "f4be": ">f", "f8be": ">d"
            }
            return fmt[self.bookmarks[bookmark][1]]
        else:
            print("Warning: trying to look up non-existing bookmark {0} in {1}".format(bookmark, self.bookmarks))
        return None

    def set_bookmark(self, bookmark, position, fmt):
        if bookmark:
            if bookmark in self.bookmarks:
                print("Warning: overwriting existing bookmark {0}. This may cause trouble later.".format(bookmark))
            self.bookmarks[bookmark] = (position, fmt)
            self.unresolved.add(bookmark)

    def write(self, format, value, buffer, bookmark=""):
        fmt = {
            "u1" : "B", "s1" : "b", "u2le" : "<H", "s2le" : "<h",
            "u4le" : "<I", "s4le" : "<i", "u8le": "<Q", "s8le" : "<q",
            "f2le" : "<e", "f4le" : "<f", "f8le" : "<d",
            "u2be": ">H", "s2be": ">h",
            "u4be": ">I", "s4be": ">i", "u8be": ">Q", "s8be": ">q",
            "f2be": ">e", "f4be": ">f", "f8be": ">d"
        }
        self.set_bookmark(bookmark, len(buffer), format)
        buffer = buffer + struct.pack(fmt[format], value)
        return buffer

    def write_into(self, bookmark, value, buffer):
        pos = self.get_bookmark_position(bookmark)
        fmt = self.get_bookmark_fmt(bookmark)
        struct.pack_into(fmt, buffer, pos, value)
        #print(self.unresolved)
        self.unresolved.remove(bookmark)
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
        formatstr = "{0}s".format(len(value))
        self.set_bookmark(bookmark, len(buffer), formatstr)
        buffer = buffer + struct.pack(formatstr, value.encode(encoding))
        return buffer

    def get_unresolved(self):
        return self.unresolved
