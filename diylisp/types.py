# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""

import operator
from functools import partial

class LispError(Exception): 
    """General lisp error class."""
    pass

class Closure:
    
    def __init__(self, env, params, body):
        if not isinstance(params, list):
            raise LispError("Parameters should be a list")

        self.env = env
        self.params = params
        self.body = body

    def __str__(self):
        return "<closure/%d>" % len(self.params)

def _arithmetic_function(op, *args):
    try:
        casted_args = map(int, args)
    except ValueError:
        raise LispError("Arguments to arithmetic function must be numbers")

    return op(casted_args[0], casted_args[1])

class Environment:

    def __init__(self, variables=None):
        from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer

        self.variables = variables if variables else {}

        arithmetic = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.div,
            'mod': operator.mod,
            '<': operator.lt,
            '<=': operator.le,
            '>': operator.gt,
            '>=': operator.ge,
        }
        
        for op, fun in arithmetic.iteritems():
            self.variables[op] = partial(_arithmetic_function, fun)
        
        self.variables['eq'] = lambda x, y: is_atom(x) and is_atom(y) and x == y

    def lookup(self, symbol):
        if symbol in self.variables:
            return self.variables[symbol]
        else:
            raise LispError("Undefined symbol " + symbol)

    def extend(self, variables):
        current_vars = self.variables.copy()
        current_vars.update(variables)
        return Environment(current_vars)

    def set(self, symbol, value):
        if symbol in self.variables:
            raise LispError("Symbol " + symbol + " was already defined")

        self.variables[symbol] = value
