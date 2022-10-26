

import sys
path = sys.argv[1]
with open(path, 'r') as f:
    string = f.read()
    print(string)
    