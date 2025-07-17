import sympy
import pytest
from genetic import Genetic, is_power_of_two
from chromosome import Chromosome
from params import Params


def create_symbols(expr: str):
    return list(sympy.sympify(expr).free_symbols)

def auxiliar_populacao_inicial():
    symbols = create_symbols("x")
    expr = sympy.sympify("x**2 + 3")
    ga = Genetic(Params, symbols, expr)

    return ga

def test_retorno_batch_fitness():
    ga = auxiliar_populacao_inicial()
    genes = [[0], [1], [2]]
    values = ga.batch_fitness(genes)
    expected = [3.0, 4.0, 7.0]

    assert all(abs(a - b) < 1e-6 for a, b in zip(values, expected))


def test_batch_fitness_validade_genes():
    expr = sympy.sympify("x + y")
    symbols = create_symbols("x + y")
    ga = Genetic(Params, symbols, expr)
    genes = [[1], [2]]

    try:
        ga.batch_fitness(genes)
        assert False
    except ValueError:
        assert True

def test_tamanho_populacao_atual1():
    ga = auxiliar_populacao_inicial()
    ga.population = ga.population[:2]
    resultado = ga.next_generation()
    assert len(resultado) == 2

def test_tamanho_populacao_atual2():
    symbols = create_symbols("x")
    expr = sympy.sympify("x**2 + 3")
    ga = Genetic(Params, symbols, expr)
    ga.population = [Chromosome.random(Params,symbols,10) for i in range(32)]
    resultado = ga.next_generation()
    assert len(resultado) == 32

def test_validar_populacao_size_nao_potencia_de_2():
    params = Params
    params.POPULATION_SIZE = 30
    with pytest.raises(ValueError, match="Population size must be a power of 2"):
        Genetic(params, create_symbols("x"), sympy.sympify("x"))

def test_validar_params_rate_negativa():
    params = Params
    params.POPULATION_SIZE = 32
    params.ELITISM_RATE = -0.1 
    with pytest.raises(ValueError, match="Rates must be positive"):
        Genetic(params, create_symbols("x"), sympy.sympify("x"))

def test_validar_soma_taxas_maior_que_1():
    params = Params
    params.POPULATION_SIZE = 32
    params.ELITISM_RATE = 0.5
    params.TOURNAMENT_RATE = 0.3
    params.CROSSOVER_RATE = 0.3
    params.LOTTERY_RATE = 0.1
    with pytest.raises(ValueError, match="sum of the rates"):
        Genetic(params, create_symbols("x"), sympy.sympify("x"))

class Parametros(Params):
    ELITISM_RATE = 0.2
    TOURNAMENT_RATE = 0.2
    CROSSOVER_RATE = 0.2
    LOTTERY_RATE = 0.1
    TOURNAMENT_SIZE = 64
    POPULATION_SIZE = 32

def test_validate_params_torneio_maior_que_populacao():
    with pytest.raises(ValueError, match="Tamanho do torneio"):
        Genetic(Parametros, symbols=[], expr=None)