from chromosome import Chromosome
from params import Params
import sympy

def create_symbols(expr):
    text = sympy.sympify(expr)
    symbols = list(text.free_symbols)
    return symbols


def test_ini():
    symbols = create_symbols("x+2")
    c = Chromosome(Params, symbols, [0.2])
    assert isinstance(c, Chromosome) 

def test_random():
    symbols = create_symbols("x+2")
    c = Chromosome.random(Params, symbols, 3.0)
    
    assert isinstance(c, Chromosome) 
    assert len(c.genes) == 1

def test_random_with_two_variables():
    symbols = create_symbols("x+y+2")
    c = Chromosome.random(Params, symbols, 4.0)
    assert isinstance(c, Chromosome) 
    assert len(c.genes) == 2

def test_without_symbol():
    symbols = create_symbols("2")
    try:
        c = Chromosome(Params, symbols, [0.2])
        assert False
    except ValueError:
        assert True

def test_more_than_two_symbol():
    symbols = create_symbols("x+y+z")
    try:
        c = Chromosome(Params, symbols, [0.2])
        assert False
    except ValueError:
        assert True

def test_str():
    symbols = create_symbols("x")
    c = Chromosome(Params, symbols, [0.2])
    assert str(c) == f"Chromosome: {[0.2]}"

def test_depth():
    symbols = create_symbols("x")
    c = Chromosome(Params, symbols, [51])
    assert c.genes == [Params.DEPTH]

def test_depth_negative():
    symbols = create_symbols("x")
    c = Chromosome(Params, symbols, [-74])
    assert c.genes == [-Params.DEPTH]

def test_fitness():
    expr_txt = "x^2 + 5"
    symbols = create_symbols(expr_txt)
    expr = sympy.sympify(expr_txt)

    x = 2
    c = Chromosome(Params, symbols, [x])

    value = x**2 + 5
    assert c.fitness(expr) == float(value)

def test_fitness_with_two_variables():
    expr_txt = "x^2 + 3*y + 5"
    expr = sympy.sympify(expr_txt)
    symbols = sorted(create_symbols(expr_txt), key = lambda s: s.sort_key())

    x = 2
    y = 4
    c = Chromosome(Params, symbols, [x, y])

    value = x**2 + 3*y + 5
    assert c.fitness(expr) == float(value)

def test_crossover_with_different_sizes():
    symbols = create_symbols("x")
    c1 = Chromosome(Params, symbols, [0.5])
    symbols = create_symbols("x+y")
    c2 = Chromosome(Params, symbols, [0.2, 0.1])

    try:
        c3 = c1.crossover(c2)
        assert False
    except ValueError:
        assert True

def test_crossover_with_one_size():
    symbols = create_symbols("x")
    c1 = Chromosome(Params, symbols, [0.5])
    symbols = create_symbols("y")
    c2 = Chromosome(Params, symbols, [0.7])

    c3 = c1.crossover(c2)
    assert c3.genes == [(0.5+0.7)/2]

def test_crossover_with_two_size():
    symbols = create_symbols("x**2 + 5*y")
    c1 = Chromosome(Params, symbols, [0.5, 0.23])
    symbols = create_symbols("y^3 + 6*x + 7")
    c2 = Chromosome(Params, symbols, [0.7, 1.4])

    c3 = c1.crossover(c2)
    assert c3.genes == [0.5, 1.4]

def test_mutate():
    symbols = create_symbols("x**2 + 5*y")
    c = Chromosome(Params, symbols, [0.5, 0.23])

    c_mutate = c.mutate(5)
    assert c_mutate.genes != c.genes

