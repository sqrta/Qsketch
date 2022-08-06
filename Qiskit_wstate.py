from qiskit import QuantumCircuit
from qiskit import gate

circuit = QuantumCircuit(3)

# Spec {qubit:2, initial: 00} 
circuit.ry(??, 0)

circuit.control(0,1,h)
# Spec {final: 1/sqrt(3) (00+01+10)}