import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr): #looks up symbols in the current environment
        return env.lookup(expr)
    elif self_evaluating(expr): #returns self-evaluating expressions (such as numbers)
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest #***
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env) #evaluates special forms
    else:
        # BEGIN PROBLEM 3
        # Evaluate the operator (which should evaluate to a Procedure instance).
        operator = scheme_eval(first, env)
        # Evaluate all of the operands and collect the results (the argument values) in a Scheme list.
        new_pair = rest.map(lambda x: scheme_eval(x, env))
        return scheme_apply(operator, new_pair, env)
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        
        # convert args (Scheme list) into a Python list:
        py_list = []
        copy_args = args
        while copy_args: #cannot do copy_args.rest bc skips over something
            py_list.append(copy_args.first)
            copy_args = copy_args.rest
        
        # If procedure.need_env is True, then add the current environment env as the last argument to this Python list.
        if procedure.need_env:
            py_list.append(env)

        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
                # call procedure.py_func on those arguments?
            return procedure.py_func(*py_list)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        
        #first need to find env in which lambda was defined--> make_child
        lambda_env = procedure.env.make_child_frame(procedure.formals, args)
        # then eval within that frame
        return eval_all(procedure.body, lambda_env)

        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        mu_env = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, mu_env) #same thing as the lambda thing except with defined mu procedure
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    expressions_copy = expressions
    if expressions_copy is nil: #read the question
        return None
    elif expressions.rest is nil:
        return scheme_eval(expressions_copy.first, env)
    else:
        scheme_eval(expressions_copy.first, env)
        return eval_all(expressions_copy.rest, env) #return the last one
    # END PROBLEM 6


##################
# Tail Recursion #
##################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
