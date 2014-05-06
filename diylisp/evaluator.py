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
    elif is_symbol(ast):
        return env.lookup(ast)
    elif is_list(ast):
        f = ast[0]
        params = ast[1:]

        if is_list(f):
            c = evaluate(f, env)
            return evaluate([c] + params, env)
        elif f == 'quote':
            return params[0]
        elif f == 'atom':
            return is_atom(evaluate(params[0], env))
        elif f == 'if':
            test = evaluate(params[0], env)
            if not is_boolean(test):
                raise LispError("First argument to if must be boolean")

            if test:
                return evaluate(params[1], env)
            else:
                return evaluate(params[2], env)
        elif f == 'define':
            if len(params) != 2:
                raise LispError("Wrong number of arguments")
            elif not is_symbol(params[0]):
                raise LispError("First argument to define is a non-symbol")
            env.set(params[0], evaluate(params[1], env))
        elif f == 'lambda':
            if len(params) != 2:
                raise LispError("Wrong number of arguments")
            return Closure(env, params[0], params[1])
        elif is_closure(f):
            evaled_params = {}
            for i, symbol in enumerate(f.params):
                evaled_params[symbol] = evaluate(params[i], f.env)
            
            closure_env = f.env.extend(evaled_params)

            return evaluate(f.body, closure_env)
        elif is_symbol(f):
            evaled = evaluate(f, env)
            evaled_params = []
            for p in params:
                evaled_params.append(evaluate(p, env))
            
            if callable(evaled):  # python function 
                return evaled(*evaled_params)
            elif is_closure(evaled):
                expected_arg_length = len(evaled.params)
                actual_arg_length = len(evaled_params)
                if expected_arg_length != actual_arg_length:
                    raise LispError("wrong number of arguments, expected " + str(expected_arg_length) + " got " + str(actual_arg_length))
                return evaluate([evaled] + evaled_params, evaled.env)
            else:
                raise LispError()
        else:
            raise LispError(str(ast) + "is not a function")
    else:
        raise LispError("xxx")
