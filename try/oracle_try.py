from qiskit.aqua.components.oracles import TruthTableOracle, LogicalExpressionOracle

expression = 'Or(And(v0, v1, v2), And(~v0, ~v1, ~v2))'
oracle=LogicalExpressionOracle(expression, optimization=True)
circ= oracle.circuit.decompose()
print(circ)
print(circ.data)
# print(oracle.circuit)
# print(oracle.circuit.data)