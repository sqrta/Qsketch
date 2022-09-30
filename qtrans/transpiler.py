from ast import *
import re
import tokenize
import io
import spec_conventions

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
    args, body = args_and_body
    for statement in body:
        match statement:
            case Expr(value=Call(
                            func=Name(id='f', ctx=Load()),
                            args=[
                                Name(id='a', ctx=Load())],
                            keywords=[])):
                expr: Expr = statement
                expr.value
                pass
            
    return