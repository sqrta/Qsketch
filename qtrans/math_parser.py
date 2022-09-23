import math
import ply
import ply.yacc as yacc
import ply.lex as lex
import sys

# From example https://github.com/dabeaz/ply/blob/master/example/calc/calc.py

special_num_map = {
    '₀': '0', '⁰': '0', '0': '0',
    '₁': '1', '¹': '1', '1': '1',
    '₂': '2', '²': '2', '2': '2',
    '₃': '3', '³': '3', '3': '3',
    '₄': '4', '⁴': '4', '4': '4',
    '₅': '5', '⁵': '5', '5': '5',
    '₆': '6', '⁶': '6', '6': '6',
    '₇': '7', '⁷': '7', '7': '7',
    '₈': '8', '⁸': '8', '8': '8',
    '₉': '9', '⁹': '9', '9': '9'
}

tokens = (
    'NUMBER', 'NUMBASE', 'NUMEXP', 
    'SIN', 'COS', 'TAN', 'ASIN', 'ACOS', 'ATAN', 
    'SQRT', 
    'EXP', 
    'VECLABEL',
    'PI', 'E', 'I'
)

literals = ['+', '-', '*', '/', '^', '(', ')', '[', ']', '{', '}', '√', '|', '>', '⟩']

# Tokens

# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_SIN = r'sin'
t_COS = r'cos'
t_TAN = r'tan'
t_ASIN = r'asin'
t_ACOS = r'acos'
t_ATAN = r'atan'
t_SQRT = r'sqrt'
t_EXP = r'exp'
t_PI = r'pi|π'
t_E = r'e'
t_I = r'i'
t_NUMBASE = r'\d+'
t_NUMEXP = r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+'
t_VECLABEL = r'\|[01]+[>⟩]'

def to_num(s):
    return int(''.join(map(lambda c: special_num_map[c], s)))

def t_NUMBER(t):
    r'[\d⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉₀]+'
    t.value = complex(to_num(t.value))
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
    ('right', 'USQRT'),
    ('left', '^')
)

# dictionary of names
names = {}

# def p_statement_assign(p):
#     'statement : NAME "=" expression'
#     names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : vectorexpr'
    return p[1]


def p_expression_binop(p):
    '''
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
               | expression '^' expression
               | expression     expression
    '''
    if p[2] == '+':
        p[0] = ('add_s', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('minus_s', p[1], p[3])
    elif p[2] == '*':
        p[0] = ('mult_s', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('div_s', p[1], p[3])
    elif p[2] == '^':
        p[0] = ('pow', p[1], p[3])
    else:
        p[0] = ('mult_s', p[1], p[2])

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = ('neg', p[2])

def p_group_expression(p):
    "expression : group"
    p[0] = p[1]

def p_expression_trig(p):
    '''
    expression : SIN group
               | COS group
               | TAN group
               | ASIN group
               | ACOS group
               | ATAN group
    '''
    p[0] = (p[1], p[2])

def p_expression_exp(p):
    '''
    expression : EXP group
    '''
    p[0] = ('exp', p[2])

def p_expression_pow(p):
    '''
    expression : NUMBASE NUMEXP
    '''
    p[0] = ('pow', complex(to_num(p[1])), complex(to_num(p[2])))

# ¹/₂√2π²|00⟩
def p_expression_sqrt(p):
    '''
    expression : SQRT group
    '''
    p[0] = ('sqrt', p[2])

def p_expression_usqrt(p):
    '''
    expression : '√' expression %prec USQRT
    '''
    p[0] = ('sqrt', p[2])

def p_expression_group(p):
    '''
    group : '(' expression ')'
          | '[' expression ']'
          | '{' expression '}'
    '''
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_const(p):
    '''
    expression : PI
               | 'π'
               | E
               | I
    '''
    if p[1] == 'π':
        p[0] = complex(math.pi, 0)
    elif p[1] == 'e': 
        p[0] = complex(math.e, 0)
    elif p[1] == 'i':
        p[0] = complex(0, 1)

def p_vectorexpr_basis(p):
    '''
    vectorexpr : VECLABEL
    '''
    p[0] = ('vec', p[1][1 : -1])

def p_expression_uminus(p):
    "vectorexpr : '-' vectorexpr %prec UMINUS"
    p[0] = ('mult_v', complex(-1, 0), p[2])

def p_vectorexpr_binop(p):
    '''
    vectorexpr : vectorexpr '+' vectorexpr
               | vectorexpr '-' vectorexpr
               | expression '*' vectorexpr
               | expression     vectorexpr
               | vectorexpr '/' expression
    '''
    if p[2] == '+':
        p[0] = ('add_v', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('minus_v', p[1], p[3])
    elif p[2] == '*':
        p[0] = ('mult_v', p[1], p[3])
    elif p[2] == '/':
        p[0] = ('mult_v', ('div_s', 1, p[3]), p[1])
    else:
        p[0] = ('mult_v', p[1], p[2])

def p_vectorexpr_group(p):
    '''
    vectorexpr : '(' vectorexpr ')'
               | '[' vectorexpr ']'
               | '{' vectorexpr '}'
    '''
    p[0] = p[2]

# def p_expression_name(p):
#     "expression : NAME"
#     try:
#         p[0] = names[p[1]]
#     except LookupError:
#         print("Undefined name '%s'" % p[1])
#         p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parse(s):
    return yacc.parse(s)

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    print(yacc.parse(s))
