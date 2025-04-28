import math
import operator as op

from definitions import SYMBOL, NUMBER, LIST

# Constants for 32-bit integer limits
INT32_MAX = 2**31 - 1  # 2,147,483,647
INT32_MIN = -2**31     # -2,147,483,648

def check_int32_overflow(value):
				"""Check if a value exceeds the 32-bit integer range."""
				if isinstance(value, int) and (value > INT32_MAX or value < INT32_MIN):
								raise OverflowError(f"Value {value} exceeds 32-bit integer range")
				return value

def safe_add(a, b):
				result = op.add(a, b)
				return check_int32_overflow(result)

def safe_sub(a, b):
				result = op.sub(a, b)
				return check_int32_overflow(result)

def safe_mul(a, b):
				result = op.mul(a, b)
				return check_int32_overflow(result)

def safe_pow(a, b):
				result = pow(a, b)
				return check_int32_overflow(result)

def safe_abs(x):
				result = abs(x)
				return check_int32_overflow(result)

class Environment:
				"""
				Environment class for storing and retrieving variables in a nested context.
				"""
				def __init__(self, outer=None):
								"""
								Initialize a new Environment.

								Parameters:
												outer (Environment, optional): The outer environment (parent scope). Defaults to None.
								"""
								self.variables = {}
								self.outer = outer

				def find(self, var):
								"""
								Find the innermost Environment where var appears.

								Parameters:
												var (str): The variable name to look up.

								Returns:
												Environment: The environment where the variable is defined.

								Raises:
												NameError: If the variable is not found in this environment or any outer environment.
								"""
								if var in self.variables:
												return self
								elif self.outer:
												return self.outer.find(var)
								else:
												raise NameError(f"Undefined variable: {var}")


class Procedure(object):
				def __init__(self, params, body, env):
								self.params = params
								self.body = body
								self.env = env
				def __call__(self, *args):
								inner_env = Environment(outer=self.env)
								for param, arg in zip(self.params, args):
												inner_env.variables[param] = arg
								return eval(self.body, inner_env)


global_env = Environment()
global_env.variables = {
								'+':safe_add, '-':safe_sub, '*':safe_mul, '/':op.truediv,
								'>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
								'abs':     safe_abs,
								'append':  op.add,
								'apply':   lambda proc, args: proc(*args),
								'begin':   lambda *x: x[-1],
								'car':     lambda x: x[0],
								'cdr':     lambda x: x[1:],
								'cons':    lambda x,y: [x] + (y if isinstance(y, LIST) else [y]),
								'eq?':     op.is_,
								'expt':    safe_pow,
								'equal?':  op.eq,
								'length':  len,
								'list':    lambda *x: LIST(x),
								'list?':   lambda x: isinstance(x, LIST),
								'map':     map,
								'max':     max,
								'min':     min,
								'not':     op.not_,
								'or':      op.or_,
								'and':     op.and_,
								'null?':   lambda x: x == [],
								'number?': lambda x: isinstance(x, NUMBER),
								'print':   print,
								'procedure?': callable,
								'round':   round,
								'symbol?': lambda x: isinstance(x, SYMBOL),
								'T': True,
								'NIL': False,
								'mapcar': lambda symbol, *lists: [
									eval([symbol] + list(items), Environment(outer=global_env))
									for items in zip(*lists)
								],
}
global_env.variables.update(vars(math)) # sin, ...

def eval(x, env=global_env):
				"""
				Evaluate a Lisp expression in an environment.

				Args:
								x: The expression to evaluate
								env: The environment in which to evaluate the expression (default: global_env)

				Returns:
								The result of evaluating the expression
				"""
				if isinstance(x, SYMBOL):    # variable reference
								return env.find(x).variables[x]
				elif not isinstance(x, LIST):# constant
								return x
				elif x[0] == 'quote':            # quotation
								(_, exp) = x
								return exp
				elif x[0] == 'if':             # conditional
								(_, test, conseq, alt) = x
								exp = (conseq if eval(test, env) else alt)
								return eval(exp, env)
				elif x[0] == 'define':         # definition
								(_, symbol, exp) = x
								env.variables[symbol] = eval(exp, env)
				elif x[0] == 'set!':           # assignment
								(_, symbol, exp) = x
								env.find(symbol).variables[symbol] = eval(exp, env)
								return env.find(symbol).variables[symbol]
				elif x[0] == 'lambda':         # procedure
								(_, params, body) = x
								return Procedure(params, body, env)
				elif x[0] == 'defun':
								(_, symbol, params, body) = x
								env.variables[symbol] = Procedure(params, body, env)
				else:                        # procedure call
								proc = eval(x[0], env)
								vals = [eval(arg, env) for arg in x[1:]]
								return proc(*vals)
