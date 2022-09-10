# S := int | S + S | S - S | sqrt(S) | arcsin(S) | S / S

import ast
from cmath import sqrt
import time
from cmath import asin as arcsin
from bs4 import ResultSet
import numpy as np
from treelib import Tree
import copy
import random

NONTERMINAL = 0
BOP = 1
INT = 2
UOP = 3

GlobalDepth = 6
upbound = 3
queue = []

class Node():
    def __init__(self, type, value, depth=0) -> None:
        self.type = type
        self.value = value
        self.depth = depth

    def Is_NonTerminal(self):
        return self.type==NONTERMINAL

    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return self.__str__()

class pattern():
    def __init__(self, root, siblings) -> None:
        self.root = root
        self.siblings = siblings

def GetTerminateRules(low=0, high=5):
    return [pattern((INT, str(i)), []) for i in range(low, high+1)]

TerminateRules = GetTerminateRules(0,upbound)

NonTerminateRules={
    '+':pattern((BOP, '+'), [(NONTERMINAL, 'S1'), (NONTERMINAL, 'S2')]),
    '/':pattern((BOP, '/'), [(NONTERMINAL, 'S1'), (NONTERMINAL, 'S2')]),
    '*':pattern((BOP, '*'), [(NONTERMINAL, 'S1'), (NONTERMINAL, 'S2')]),
    'sqrt':pattern((UOP, 'sqrt'), [(NONTERMINAL, 'S')]),
    'arcsin':pattern((UOP, 'arcsin'), [(NONTERMINAL, 'S')]),
}

#Rules = TerminateRules + NonTerminateRules

class Expression():
    def __init__(self, root_node):
        self.ast = Tree()
        self.ast.create_node(tag='Root',identifier='root', data=root_node)
        self.NonTerminals = []
        self.depth=0
        if root_node.Is_NonTerminal():
            self.NonTerminals.append('root')

    def Have_Nonterminal(self):
        return len(self.NonTerminals)>0

    def DecideRules(self, uid):
        rootDepth = self.ast[uid].data.depth
        NTPart = copy.deepcopy(NonTerminateRules)
        TPart = GetTerminateRules(0,upbound)
        if self.ast[uid].is_root():
            return list(NTPart.values()) + TPart 

        parentNode = self.ast.parent(uid).data
        if parentNode.value=='sqrt':
            TPart = GetTerminateRules(2,upbound)
            NTPart.pop('sqrt')
        elif parentNode.value == 'arcsin':
            TPart = GetTerminateRules(0,1)
            NTPart.pop('arcsin')
        elif parentNode.value == '+':
            TPart = GetTerminateRules(1,upbound)
            NTPart.pop('+')
        elif parentNode.value =='/':
            NTPart.pop('/')
            TPart = GetTerminateRules(1,upbound)
        elif parentNode.value == '*':
            NTPart.pop('*')
            TPart = GetTerminateRules(2,upbound)

        if self.depth >= GlobalDepth:
            NTPart = {}
        
        return list(NTPart.values()) + TPart


    def product(self):
        # self.expr = [NonTerminal('S'), Terminal('+'), NonTerminal('S')]
        result = []
        choice = random.randint(0, len(self.NonTerminals)-1)
        uid = self.NonTerminals[choice]
        rootDepth = self.ast[uid].data.depth
        productRules = self.DecideRules(uid)
        
        for pattern in productRules:
            rootNode = Node(pattern.root[0], pattern.root[1], rootDepth)
            siblingNodes = [Node(i[0], i[1], rootDepth+1) for i in pattern.siblings]
            NewExpr = copy.deepcopy(self)
            NewExpr.ast[uid].data = rootNode
            NewExpr.ast[uid].tag = str(rootNode.value)
            NewExpr.depth=self.depth+1
            for sibling in siblingNodes:
                tmp = NewExpr.ast.create_node(tag=str(sibling.value),parent=uid, data=sibling)
                if sibling.type==NONTERMINAL:
                    NewExpr.NonTerminals.append(tmp.identifier)
            if rootNode.type!=NONTERMINAL:
                NewExpr.NonTerminals.remove(uid)

            result.append(NewExpr)

        return result
        # list of Expression
    def __str__(self):
        return str(self.ast)
    def __repr__(self):
        return self.__str__()

def EvalExpr(expr):
    def Eval(rootData, siblings):
        #print(rootData, siblings)
        if rootData.type == INT:
            return rootData.value
        elif rootData.value=='+':
            return '('+siblings[0]+'+'+siblings[1]+')'
        elif rootData.value=='/':
            return siblings[0]+'/'+siblings[1]
        elif rootData.value=='*':
            return siblings[0]+'*'+siblings[1]
        elif rootData.value == 'sqrt':
            return 'sqrt('+siblings[0]+')'
        elif rootData.value == 'arcsin':
            return 'arcsin('+siblings[0]+')'
        else:
            return rootData.value
    def EvalTree(ast, root):
        siblings = [EvalTree(ast, i) for i in list(ast.children(root.identifier))]
        return Eval(root.data, siblings)
    return EvalTree(expr.ast, expr.ast[expr.ast.root])

S = Node(NONTERMINAL, 'S')
start = Expression(S)

queue.append(start)

def verify(candidate, to_code, goal):
    result = EvalExpr(candidate)
    # print(result)
    code = to_code(result)
    return exec(code) == goal

    # if len(result)>=2 and result[0]=='2' and result[1]=='/':
    #     print(result)

def solve_scl(callback, goal):
    # startTime = time.time()
            
    while len(queue)>0:
        candidate = queue.pop(0) # candiate: Expression
        #print(EvalExpr(candidate))
        
        if not candidate.Have_Nonterminal():
            if verify(candidate, callback, goal):
                break
        else:
            expressions = candidate.product()
            for expression in expressions:
                queue.append(expression)
    # endTime = time.time()
    # print("Use {0}s.".format(endTime-startTime))
