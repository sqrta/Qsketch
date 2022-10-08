from ast import *

test = '''
# circ.__1(__, 0)
# ch0=HGate().control(ctrl_state=0)
circ.append(ch0, [0,1])
'''

parsed = parse(test)
func = parsed.body[0]
ab = 'a' + 'b'

print(dump(parsed, indent=4))

match func:
    case Expr(
        value=Call(
            func=Attribute(
                value=Name(id=ab),
                attr='__1'),
            args=[
                Name(id='__'),
                Constant(value=0)]
            )
        ):
        print("yes")

