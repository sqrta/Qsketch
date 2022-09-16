import re
import ply
import tokenize

def get_init_state(comment: str):
    prefix = re.match("(#+\s*)+Spec\s*", comment)
    spec = comment[prefix.end() + 1 :]
    dict = eval(spec)
    return dict["initial"]

def get_res_state():
    pass

