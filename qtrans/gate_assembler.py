from typing import Callable
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import BasicAer

def assemble_single(op):
    match op:
        case ('x', _, q): return lambda qc: qc.x(q)
        case ('y', _, q): return lambda qc: qc.y(q)
        case ('z', _, q): return lambda qc: qc.z(q)
        case ('rx', t, q): return lambda qc: qc.rx(t, q)
        case ('ry', t, q): return lambda qc: qc.ry(t, q)
        case ('rz', t, q): return lambda qc: qc.rz(t, q)
        case ('h', _, q): return lambda qc: qc.h(q)

def assemble(manifest, qc: QuantumCircuit) -> Callable[[QuantumRegister | list[QuantumRegister]]]:
    res = []
    for op in manifest:
        res.append(assemble_single(op)(qc))
    return res
