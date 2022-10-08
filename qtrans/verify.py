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
