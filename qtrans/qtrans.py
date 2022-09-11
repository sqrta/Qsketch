import io
import sys
import re
import tokenize

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
    tokens = [token for token in tokenize.generate_tokens(io.StringIO(s).readline)]
    wildcards = list(filter(lambda t: t.string == "__", tokens))
    indexed_holes = list(filter(lambda t: re.match("^__\d+$", t.string) is not None, tokens))
    indices = []
    indices = sorted(set(map(lambda t: int(t.string[2 :]), indexed_holes)))
    
    steps = []
    pointer = 0
    for i in indices:
        def l(stri, p):
            return lambda ts: fill_single(ts, "__" + stri, p)
        steps.append(l(str(i), params[pointer]))
        # if i in indices:
        #     for m in re.finditer("__" + str(i), s):
        #         steps.append(lambda: modify_in_place(m.start(), m.end(), s, params[pointer]))
        
        pointer = pointer + 1

    for step in steps:
        tokens = step(tokens)
    steps = []

    for hole in wildcards:
        i = tokens.index(hole)
        tokens.remove(hole)
        tokens.insert(i, hole._replace(string = params[pointer]))
        
        if (pointer < len(params)):
            pointer = pointer + 1
        else:
            break
    # for m in re.finditer("__", s):
    #     steps.append(modify_in_place(m.start(), m.end(), s, params[pointer]))
    #     if (pointer < len(params)):
    #         # wildcards[i] = params[pointer]
    #         pointer = pointer + 1
    #     else:
    #         break

    # for step in steps:
    #     s = step()
    # steps = []

    return tokenize.untokenize(tokens)
    
    # mat_hole_span = re.search("??(", s).span()
    # to_full_str = lambda v: s.replace("??", str(v))
    
    # if mat_hole_span != (0, 0):
    #     # TODO
    #     pass
    # else:
    #     return demo.solve_scl(to_full_str)
        # scl_hole_span = re.search("??", s).span()

def fill_single(tokens: list[tokenize.TokenInfo], hole: str, value: str):
    # tokens = [token for token in tokenize.generate_tokens(io.StringIO(input).readline)]
    return list(map(lambda t: t._replace(string = value) if t.string == hole else t, tokens))

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
    ret = fill_in_hole("test __2 __3 __ __5 __ __3 __", ["a", "b", "c", "d", "e", "f"])
    pass
    # open_file_with(fill_in_hole)
