# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

binary_forms = ['eq', '+', '-', '*', '/', 'mod', '>', '<', '>=', '<=']

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_boolean(ast) or is_integer(ast):
        return ast
    elif is_list(ast):
        f = ast[0]
        params = ast[1:]
        if f == 'quote':
            return params[0]
        elif f == 'atom':
            return is_atom(evaluate(params[0], env))
        elif f == 'if':
            test = evaluate(params[0], env)
            if not is_boolean(test):
                raise LispError("First param to if must be boolean")

            if test:
                return evaluate(params[1], env)
            else:
                return evaluate(params[2], env)

        elif f in binary_forms:
            first = evaluate(params[0], env)
            second = evaluate(params[1], env)

            if f == 'eq':   
                return is_atom(first) and is_atom(second) and first == second
            else:
                if not is_integer(first) or not is_integer(second):
                    raise LispError("Operands to " + f + " must be integers")

                if f == '+':
                    return first + second
                elif f == '-':
                    return first - second
                elif f == '/':
                    return first / second
                elif f == '*':
                    return first * second
                elif f == 'mod':
                    return first % second
                elif f == '>':
                    return first > second
                elif f == '<':
                    return first < second
                elif f == '<=':
                    return first <= second
                elif f == '>=':
                    return first >= second
