import os
import sys
from ac7parser.Ac7File import Ac7File

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def main():
    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "5-4 Jazz X700.AC7"))
    result = []
    with open(os.path.join(get_script_path(), "testfiles", "summary1.txt"), "w") as f:
        f.write("\n".join(a.summarize(result)).replace(", ", ",\n"))

    a.write_file(os.path.join(get_script_path(), "testfiles", "Result1.AC7"), allow_overwrite=True)

    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "Result1.AC7"))
    result = []
    with open(os.path.join(get_script_path(), "testfiles", "summary2.txt"), "w") as f:
        f.write("\n".join(a.summarize(result)).replace(", ", ",\n"))

if __name__ == "__main__":
    main()
