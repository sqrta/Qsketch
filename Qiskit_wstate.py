from qiskit import QuantumCircuit
from qiskit import gate
from qiskit.circuit.library.standard_gates import HGate

circ = QuantumCircuit(3)

# Spec {qubit:2, initial: 00} 
circ.??(??, 0)
ch0=HGate().control(ctrl_sstate=0)
circ.append(ch0, [0,1])
# Spec {final: 1/sqrt(3) (00+01+10)}


ry 1.2309594173407747