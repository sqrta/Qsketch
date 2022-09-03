from braket.circuits import Circuit
from braket.devices import LocalSimulator
from math import sqrt
import time
from math import asin as arcsin

import numpy as np
# apply a general unitary
my_unitary = np.array([[1,0,0,0],[0,1/2**0.5, 0,1/2**0.5],[0,0,1,0],[0,1/2**0.5, 0, -1/2**0.5]])


circ = Circuit()
circ.ry(0, 2/arcsin(1/sqrt(3)))
circ.unitary(matrix=my_unitary, targets=[0,1])

# set up device
device = LocalSimulator()

# run circuit
result = device.run(circ, shots=1000).result()
# get measurement shots
counts = result.measurement_counts
# print counts
print(counts)