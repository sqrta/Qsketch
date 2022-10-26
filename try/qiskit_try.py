from qiskit import QuantumCircuit
from qiskit import Aer, transpile
from math import sqrt,pi
import time
from qiskit.circuit.library.standard_gates import HGate
from math import asin as arcsin

circ = QuantumCircuit(3)
circ.ry(__,0)
ch0=HGate().control(ctrl_state=0)
circ.append(ch0, [0,2])

circ.measure_all()

# Transpile for simulator
simulator = Aer.get_backend('aer_simulator')
circ = transpile(circ, simulator)

# Run and get counts
result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(counts)
