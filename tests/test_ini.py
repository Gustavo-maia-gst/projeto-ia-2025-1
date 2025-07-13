from chromosome import Chromosome
from params import Params
import sympy

def test_ini():
    expr = sympy.sympify("x + 2")
    symbols = list(expr.free_symbols)
    Chromosome(Params, symbols, [0.2,0.3])
    assert True