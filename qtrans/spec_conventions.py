
# initial state
INITIAL = 'initial'

# final state
FINAL = 'final'

# circuit object name
CIRCUIT = 'circuit'

# variables not declared in scope, but passed in instead
ARGS = 'args'

VALID_GATE_CTORS = [
    'HGate', 
    'XGate', 'RXGate',
    'YGate', 'RYGate',
    'ZGate', 'RZGate'
]

TO_CTRL_VAR = 'control'

CTRL_STATE = 'ctrl_state'

SUPPORTED_GATES = {
    'HGate': 'h', 'h': 'h',
    'XGate': 'x', 'x': 'x',
    'RXGate': 'rx', 'rx': 'rx',
    'RYGate': 'ry', 'ry': 'ry',
    'RZGate': 'rz', 'rz': 'rz',
}