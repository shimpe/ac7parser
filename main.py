import os
import sys
from Ac7File import Ac7File

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def main():
    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "Bossa6.AC7"))
    a.report()

if __name__ == "__main__":
    main()