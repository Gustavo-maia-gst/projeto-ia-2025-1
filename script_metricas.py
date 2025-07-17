import sympy
import statistics
import math
import src
from src.params import Params
from src.chromosome import Chromosome
from src.genetic import Genetic
import time


funcao_simples = "-x**2 + 10"
funcao_moderada = "-(x**2 + y**2) + 10"
funcao_complexa = "sin(x) * cos(y) * exp(-(x**2 + y**2))"
funcao_mais_complexa = "-(x**2 + y**2 - cos(18*x) - cos(18*y))"

def run_single_execution(expr: sympy.Expr, symbols, params: Params, generations=50):
    ga = Genetic(params, symbols, expr)

    for _ in range(generations):
        ga.next_generation()

    best = max(ga.population, key=lambda c: c.fitness(expr))
    return float(best.fitness(expr))


def run_multiple_executions(funcao, generations):
    expr = sympy.sympify(funcao)
    symbols = list(expr.free_symbols)

    params = Params()

    start = time.perf_counter()
    ga = Genetic(params, symbols, expr)

    for _ in range(generations):
        ga.next_generation()

    best = max(ga.population, key=lambda c: c.fitness(expr))
    fitness = float(best.fitness(expr))
    end = time.perf_counter()
    tempo = end - start

    print(f"\nGerações: {generations}")
    print(f"  Melhor fitness: {fitness:.4f}")
    print(f"  Tempo total: {tempo:.4f} segundos")


if __name__ == "__main__":
    cargas = [5, 10, 20, 40, 80, 150]
    funcoes = [funcao_simples, funcao_moderada, funcao_complexa, funcao_mais_complexa]
    for f in funcoes:
        run_multiple_executions(f, 80)
    #run_multiple_executions(funcao_mais_complexa, 30)
