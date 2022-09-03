import sys

file_path = sys.argv[1]

# print(msg)
# print(list(file))
# print('sdfdf\nsdfsd')
file = sys.path[0]+'//tmp.txt'

with open(file_path, 'r') as f:
    msg = f.read()
    msg = msg.replace("??", "1.2309594173407747")
    print(msg)