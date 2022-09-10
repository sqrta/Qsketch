import sys
import re

def open_file_with(callback):
    file_path = sys.argv[1]
    params = sys.argv[2 :]

    # print(msg)
    # print(list(file))
    # print('sdfdf\nsdfsd')
    # file = os.path.join(sys.path[0], "tmp.txt")

    with open(file_path, 'r') as f:
        print(callback(f.read(), params))

def fill_in_hole(s: str, params):
    matches = re.findall("[^a-zA-Z0-9_]__\d*[^a-zA-Z_]", s)
    wildcards = list(filter(lambda m: len(m) == 2, matches))
    indexed_holes = list(filter(lambda m: len(m) > 2, matches))
    raw_indices = list(map(lambda s: try_parse_int(s[2 :]), indexed_holes))
    indices = list(filter(lambda i: i > 0, raw_indices))
    max_index = max(indices)

    pointer = 0
    for i in range(1, max_index):
        if i in indices:
            for m in re.finditer("[^a-zA-Z0-9]__" + str(i) +"[^a-zA-Z]", s):
                s = modify_in_place(m.start(), m.end(), s, params[pointer])

            pointer = pointer + 1

    for m in re.finditer("[^a-zA-Z0-9]__[^a-zA-Z]", s):
        s = modify_in_place(m.start(), m.end(), s, params[pointer])
        if (pointer < len(params)):
            wildcards[i] = params[pointer]
            pointer = pointer + 1
        else:
            break

    return s
    
    # mat_hole_span = re.search("??(", s).span()
    # to_full_str = lambda v: s.replace("??", str(v))
    
    # if mat_hole_span != (0, 0):
    #     # TODO
    #     pass
    # else:
    #     return demo.solve_scl(to_full_str)
        # scl_hole_span = re.search("??", s).span()

def modify_in_place(start: int, end: int, old_s: str, sub: str):
    before = old_s[0 : start - 1]
    after = old_s[end + 1 :]
    return before + sub + after

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
