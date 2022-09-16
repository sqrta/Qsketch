import ply
import ply.yacc as yacc
import ply.lex as lex

# From example https://github.com/dabeaz/ply/blob/master/example/calc/calc.py

tokens = (
    'NAME', 'NUMBER',
)

literals = ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"

# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    # ('right', 'SIN', 'COS', 'TAN', 'ASIN', 'ACOS', 'ATAN', 'EXP'),
    # ('left', '^')
)

# dictionary of names
names = {'pi': 'pi', 'π': 'pi', 'e': 'e'}

# def p_statement_assign(p):
#     'statement : NAME "=" expression'
#     names[p[1]] = p[3]

def p_vector_expr(p):
    '''vexpression : sexpression '*' vexpression
                   | sexpression     vexpression
                   | vexpression '+' vexpression
                   | vexpression '-' vexpression
                   | 'T'
                   '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*' or p[2] == '×' or p[2] == '⋅':
        p[0] = p[1] * p[3]
    elif p[2] == '/' or p[2] == '÷':
        p[0] = p[1] / p[3]
    else:
        p[0] = p[1] * p[2]

def p_scalar_expression(p):
    '''sexpression : sexpression '*' sexpression
                   | sexpression     sexpression
                   | sexpression '+' sexpression
                   | sexpression '-' sexpression
                   | sexpression '/' sexpression
                   | sexpression '^' sexpression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/' or p[2] == '÷':
        p[0] = p[1] / p[3]
    else:
        p[0] = p[1] * p[2]


def p_statement_expression(p):
    'statement : sexpression'
    print(p[1])

# def p_expression_binop(p):
#     '''expression : expression '+' expression
#                   | expression '-' expression
#                   | expression '*' expression
#                   | expression expression
#                   | expression '/' expression'''
#     if p[2] == '+':
#         p[0] = p[1] + p[3]
#     elif p[2] == '-':
#         p[0] = p[1] - p[3]
#     elif p[2] == '*' or p[2] == '×' or p[2] == '⋅':
#         p[0] = p[1] * p[3]
#     elif p[2] == '/' or p[2] == '÷':
#         p[0] = p[1] / p[3]
#     else:
#         p[0] = p[1] * p[2]

def p_expression_uminus(p):
    "sexpression : '-' sexpression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    '''sexpression : '(' sexpression ')'
                   | '[' sexpression ']'
                   | '{' sexpression '}' '''
    p[0] = p[2]


def p_expression_number(p):
    "sexpression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "sexpression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = None


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)