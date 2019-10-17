import os
import sys
from ac7parser.Ac7File import Ac7File
import hashlib
from pathlib import Path

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
            if original_checksum != reconstructed_checksum:
                print("   difference found")
                failures[f] = "checksums differ"
            else:
                print("   ok")
                successes[f] = True

        except Exception as e:
            failures[f] = e.__repr__()

    for f in testfiles:
        if f not in failures:
            only_filename = os.path.basename(f)
            reconstructed_filename = os.path.join(only_folder, "reconstructed-{0}".format(only_filename))
            try:
                os.remove(reconstructed_filename)
                print("   remove after test: {0} ".format(reconstructed_filename))
            except Exception as e:
                print("   could not remove: {0}\nbecause {1} ".format(reconstructed_filename, e.__repr__()))

    print("ran {0} test".format(len(failures)+len(successes)))
    if successes:
        print("Successes: {0}".format(len(successes)))

    if failures:
        print("Failures")
        print("********")
        for f in failures:
            print("{0} because {1})".format(f,failures[f]))

if __name__ == "__main__":
    main()