import os
import sys
from ac7parser.Ac7File import Ac7File

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def main():
    a = Ac7File()
    a.load_file(os.path.join(get_script_path(), "testfiles", "Bossa6.AC7"))
    result = []
    a.summarize(result)
    print("\n".join(result))
    a.write_file(os.path.join(get_script_path(), "testfiles", "MyBossa6.AC7"), allow_overwrite=True)

if __name__ == "__main__":
    main()
