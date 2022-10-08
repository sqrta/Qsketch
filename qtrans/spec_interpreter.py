from itertools import repeat
import math
from spec_conventions import *
import math_parser

def app_expr(expression) -> complex:
    match expression:
        case ('add_s', e1, e2): return app_expr(e1) + app_expr(e2)
        case ('minus_s', e1, e2): return app_expr(e1) - app_expr(e2)
        case ('mult_s', e1, e2): return app_expr(e1) * app_expr(e2)
        case ('div_s', e1, e2): return app_expr(e1) / app_expr(e2)
        case ('pow_s', e1, e2): return app_expr(e1) ** app_expr(e2)
        case ('neg', e): return -app_expr(e)
        case ('exp', e): return complex(math.e) ** app_expr(e)
        case ('sqrt', e): return app_expr(e) ** 0.5
        case ('sin', e): return math.sin(app_expr(e).real)
        case ('cos', e): return math.cos(app_expr(e).real)
        case ('tan', e): return math.tan(app_expr(e).real)
        case ('asin', e): return math.asin(app_expr(e).real)
        case ('acos', e): return math.acos(app_expr(e).real)
        case ('atan', e): return math.atan(app_expr(e).real)

def accumulate(vec_expr, partial_c, bin: list[complex]) -> list[complex]:
    match vec_expr:
        case ('mult_v', e, v): 
            return accumulate(v, partial_c * app_expr(e), bin)
        case ('add_v', v1, v2): 
            temp = accumulate(v1, partial_c, bin)
            return accumulate(v2, partial_c, temp)
        case ('minus_v', v1, v2):
            temp = accumulate(v1, partial_c, bin)
            return accumulate(v2, -partial_c, temp)
        case ('vec', l): 
            if len(bin) == 0:
                bin = repeat(0, 2 ** len(l))
            index = int(l, 2)
            bin[index] += partial_c
            return bin

def interp(comment: str) -> dict:
    dic = eval(comment)
    if dic.has_key(INITIAL):
        dic[INITIAL] = math_parser.parse(dic[INITIAL])
    elif dic.has_key(FINAL):
        dic[FINAL] = math_parser.parse(dic[FINAL])
    return dic
    