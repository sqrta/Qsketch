from itertools import repeat
import re
import math
import math_parser
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import BasicAer

def get_init_state(comment: str):
    prefix = re.match("(#+\s*)+Spec\s*", comment)
    spec = comment[prefix.end() + 1 :]
    dict = eval(spec)
    return dict["initial"]

def get_res_state():
    pass

def init_qc(q: QuantumRegister, qc: QuantumCircuit, init_spec, use_these):
    init_state_spec = math_parser.parse(init_spec)
    res = accumulate(init_state_spec, 1, [])

    if use_these is None:
        qc.initialize(res, map(lambda i: q[i], range(0..len(res))))
    else:
        qc.initialize(res, use_these)

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