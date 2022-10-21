
from qiskit import QuantumCircuit,QuantumRegister

# Oracle 3->3->1
def mod8(x,y):
    '''
    +, -, *, %
    if then else
    '''
    if (x+y)%8==0:
        return 1
    else:
        return 0

def oracle_mod8(circ: QuantumCircuit, x: QuantumRegister(3), y: QuantumRegister(3), a: QuantumRegister(1)):
    circ.ccx(x[1], y[1], a[0])
    circ.cx(x[1], a[0])
    circ.cx(y[1], a[0])
    circ.mct([x[0],y[0],a[0]], y[2])
    circ.ccx(x[0], y[0], y[1])
    circ.cx(x[0], y[0])
    circ.cx(x[1], y[1])
    circ.cx(x[2], y[2])





