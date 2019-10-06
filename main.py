import os
import sys
from Ac7File import Ac7File

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def main():
    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "TEST0004.AC7"))
    result = []
    a.summarize(result)
    print("\n".join(result))
    a.write_file(os.path.join(get_script_path(), "testfiles", "output.ac7"), allow_overwrite=True, report_unresolved=True)

if __name__ == "__main__":
    main()