import os
import sys
from ac7parser.Ac7File import Ac7File


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def main():
    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "unlock", "BAJANLOK.AC7"))
    result = []
    with open(os.path.join(get_script_path(), "testfiles", "unlock", "BAJANLOK.txt"), "w") as f:
        f.write("\n".join(a.summarize(result)).replace(", ", ",\n"))

    a.write_file(os.path.join(get_script_path(), "testfiles", "unlock", "00BAJUNL.AC7"), allow_overwrite=True)

    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "unlock", "00BAJUNL.AC7"))
    result = []
    with open(os.path.join(get_script_path(), "testfiles", "unlock", "00BAJUNL.txt"), "w") as f:
        f.write("\n".join(a.summarize(result)).replace(", ", ",\n"))

    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "unlock", 'Straight 8-Beat CT-X3000 Fixed.AC7'))
    result = []
    with open(os.path.join(get_script_path(), "testfiles", "unlock", "straight.txt"), "w") as f:
        f.write("\n".join(a.summarize(result)).replace(", ", ",\n"))


if __name__ == "__main__":
    main()
