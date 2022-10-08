from ast import *
from mimetypes import init
import re
import tokenize
import io
from spec_conventions import *
import math_parser
import spec_interpreter

def load(string):
    module = parse(string)
    Module(
        body=[
            FunctionDef(
                name='fun',
                args=arguments(
                    posonlyargs=[],
                    args=[
                        arg(arg='x'),
                        arg(arg='y')],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]),
                body=[
                    Assign(
                        targets=[
                            Name(id='z', ctx=Store())],
                        value=Constant(value=3)),
                    Expr(
                        value=Call(
                            func=Name(id='f', ctx=Load()),
                            args=[
                                Name(id='a', ctx=Load())],
                            keywords=[])),
                    Assign(
                        targets=[
                            Name(id='r', ctx=Store())],
                        value=BinOp(
                            left=Name(id='x', ctx=Load()),
                            op=Add(),
                            right=Name(id='z', ctx=Load()))),
                    Return(
                        value=Name(id='z', ctx=Load()))],
                decorator_list=[])],
        type_ignores=[])
    func: FunctionDef = module.body[0]
    args = func.args.args
    body = func.body
    return (args, body)

# returns the initial and final spec
def get_specs(source):
    ret = []
    tokens = [token for token in tokenize.generate_tokens(io.StringIO(source).readline)]
    for token in tokens:
        prefix = re.match("(#+\s*)+Spec\s*", source)
        if prefix is None:
            continue
        else:
            spec = token[prefix.end() + 1 :]
            dict = eval(spec)
            ret.append(dict)
    return (ret[0], ret[1])

def get_bindings(specs):
    begin, _ = specs
    return begin

def transpile_body(args_and_body: tuple[list[arg], list[stmt]], external_bindings):
    arguments, body = args_and_body
    circuit_id = external_bindings[CIRCUIT]
    env = []
    manifest = []
    for statement in body:
        match statement:
            case Expr(value=Constant()):
                comment = statement.value.value
                prefix = re.match('^Spec\s*', comment)
                if prefix is not None:
                    env = spec_interpreter.interp(comment[prefix.end() + 1 :], env)

            # case: circ.append(ch0, [0,1])
            case Expr(
                value=Call(
                    func=Attribute(
                        value=Name(id=circuit_id),
                        attr='append'
                    )
                )
            ):
                manifest.append(transpile_call_append(statement, env))

            # case: circ.__1(__, ...)
            case Expr(
                value=Call(
                    func=Attribute(
                        value=Name(id=circuit_id)
                    )
                )
            ):
                expr: Expr = statement
                expr.value

            # case: ch0=HGate().control(ctrl_state=0)
            case Assign():
                env = transpile_assign(statement, env)
            
    return

class Parameter:
    def __init__(self, ctrl_state) -> None:
        self.ctrl = ctrl_state
    pass

def transpile_assign(statement: Assign, env: dict[str, Tuple[str, Parameter]]) -> list:
    gate = statement.targets[0].id
    # try get constructor name, it might not be a gate constructor and fail
    try:
        ctor_name = statement.value.func.value.func.id
        if ctor_name in VALID_GATE_CTORS:
            ctrl = get_ctrl_state(statement.value)
            gate_value = SUPPORTED_GATES[ctor_name]
            env[gate] = (gate_value, Parameter(ctrl))
    finally:
        return env

def get_ctrl_state(call: Call) -> 0 | 1 | None:
    try:
        ctrl = call.func.attr
        if ctrl is TO_CTRL_VAR and call.keywords[-1] is CTRL_STATE:
            return int(call.keywords[-1].value.value)
    except:
        return None

def transpile_call_append(statement: Expr, env: dict):
    gate = statement.value.args[0].id
    binding = env[gate]
    targets = get_value(statement.value.args[1])
    return (binding[0], binding[1], targets)

def transpile_call_std_gate(statement: Expr, env: dict) -> Tuple:
    gate_name = SUPPORTED_GATES[statement.value.func.attr]
    
    return

def get_value(node: List | Constant) -> int | list[int]:
    match node:
        case List():
            return list(map(lambda c: int(c.value), node.elts))
        case Constant():
            return int(node.value)
