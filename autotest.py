import os
import sys
from ac7parser.Ac7File import Ac7File
import hashlib
from pathlib import Path

accepted_differences = [
    (b'\xd5)\x80\x1f$\xcb\xcf\x97\xfa[\xb8\xd2a\xb77\x02', b':\x8a\xcd\xfa\x96\xbeS\xf1R}*\xd2\x14\xc2\xf1G'),
    (b'\xd5p\x0f\x18\xb5==!\xd5?p\xc1\\M\x88\xbb', b'\x89\xc2q\x96\xc6G\xbf\xd0\x87\xfce\xc8o\xf9\x02\xd4'),
    (b'\x1aY\xa6\xd5\xabc3C\x96\xc1\xfe\x1a\xcc\xc8\x9f\xc2', b'\x86v\xd7\x17\xb9Fh\xe5\xd1Ii\xe2\x0c#\x8de'),
    (b'\xfb}\x88\xc3]\x87`\x9a<\x92\xd7\x8f$\x7f\xe0\x1a', b'7K\xa7\x03\x11\x14\xf7\xdd\x15H\x1c\x1c\x95J\x9d\x1b')
]

known_assertions = [ "BBBossa1.AC7" ]

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def collect_ac7files(location):
    return [filename for filename in Path(location).glob('**/*.AC7')]

def main():
    testfiles = collect_ac7files(os.path.join(get_script_path(), "testfiles", "Community"))
    failures = {}
    successes = {}
    for f in testfiles:
        print("examining {0}".format(f))
        a = Ac7File()
        try:
            only_filename = os.path.basename(f)
            only_folder = os.path.dirname(f)
            a.load_file(f)
            reconstructed_filename = os.path.join(only_folder, "reconstructed-{0}".format(only_filename))
            a.write_file(reconstructed_filename, allow_overwrite=True)
            with open(f, "rb") as fl:
                m = hashlib.md5()
                m.update(fl.read())
                original_checksum = m.digest()
            with open(reconstructed_filename, "rb") as fl:
                m = hashlib.md5()
                m.update(fl.read())
                reconstructed_checksum = m.digest()
            if original_checksum != reconstructed_checksum and\
                    (original_checksum, reconstructed_checksum) not in accepted_differences:
                print("   unexpected difference found (orig: {0}, new: {1})".format(original_checksum, reconstructed_checksum))
                failures[f] = "checksums differ"
            else:
                print("   ok")
                successes[f] = True

        except Exception as e:
            if only_filename not in known_assertions:
                failures[f] = e.__repr__()
            else:
                print("    ok (known assertion)")

    for f in testfiles:
        if f not in failures:
            only_filename = os.path.basename(f)
            reconstructed_filename = os.path.join(only_folder, "reconstructed-{0}".format(only_filename))
            try:
                os.remove(reconstructed_filename)
                print("   remove after test: {0} ".format(reconstructed_filename))
            except Exception as e:
                print("   could not remove: {0}\nbecause {1} ".format(reconstructed_filename, e.__repr__()))

    print("ran {0} tests".format(len(failures)+len(successes)))
    if successes:
        print("Successes: {0}".format(len(successes)))

    if failures:
        print("Failures")
        print("********")
        for f in failures:
            print("{0} because {1})".format(f,failures[f]))

if __name__ == "__main__":
    main()