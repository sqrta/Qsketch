from qiskit import QuantumCircuit
from qiskit import gate
from qiskit.circuit.library.standard_gates import HGate
import qiskit.circuit.library.standard_gates

circ = QuantumCircuit(3)

# Spec { 'qubit':2, 'initial': |00> } 
circ.__1(__, 0)
circ.rx(1, 0)
ch0=HGate().control(ctrl_state=0)
circ.append(ch0, [0,1])
# Spec { final: ¹/√3 (|00⟩ + |01⟩ + |10⟩) }
