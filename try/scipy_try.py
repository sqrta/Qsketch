from scipy.optimize import minimize
import numpy as np
from math import cos,sin,pi,sqrt
from math import asin as arcsin

def Ry(theta):
    return np.array([
        [cos(theta/2), -sin(theta/2)],
        [sin(theta/2), cos(theta/2)]
    ])


initial = np.array([1,0,0,0])
final = np.array([sqrt(2)/sqrt(3), 0, sqrt(1)/sqrt(3), 0])

def f(x):
    gate = np.kron(Ry(x), I)
    norm = np.linalg.norm(gate.dot(initial)- final)
    return norm

theta = 2*arcsin(1/sqrt(3))
I = np.array([
    [1,0],
    [0,1]
])
gate = np.kron(Ry(theta), I)
print(gate.dot(initial))
print(f(0))
mymin = minimize(f,0, method="BFGS")
print(mymin)
print(theta)