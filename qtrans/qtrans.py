import sys
import re
import os
import demo
import ast

def open_file_with(callback):
    file_path = sys.argv[1]
    params = sys.argv[2:]

    # print(msg)
    # print(list(file))
    # print('sdfdf\nsdfsd')
    # file = os.path.join(sys.path[0], "tmp.txt")

    with open(file_path, 'r') as f:
        print(callback(f.read(), params))

def fill_in_hole(s: str, params):
    code : ast.Module = ast.parse(str)
    matches = re.search("__\d*", str)
    wildcards = filter(lambda m: len(m) == 2, matches)
    indexed_holes = filter(lambda m: len(m) > 2, matches)
    raw_indices = map(lambda s: try_parse_int(s[2:]), indexed_holes)
    indices = filter(lambda i: i > 0, raw_indices)
    max_index = max(indices)

    pointer = 0
    for i in range(1, max_index):
        if i in indices:
            indices = map(lambda j: params[pointer] if j == i else j)
            pointer = pointer + 1

    for i in range(pointer, len(params)):
        wildcards[i] = params[i]
    # mat_hole_span = re.search("??(", s).span()
    # to_full_str = lambda v: s.replace("??", str(v))
    
    # if mat_hole_span != (0, 0):
    #     # TODO
    #     pass
    # else:
    #     return demo.solve_scl(to_full_str)
        # scl_hole_span = re.search("??", s).span()

def try_get_mat():
    return

def try_get_scl():
    return

def try_parse_int(s):
    try:
        return int(s)
    except ValueError:
        return -1

if __name__ == "__main__":
    open_file_with(fill_in_hole)
