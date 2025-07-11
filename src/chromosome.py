from abc import ABC, abstractmethod
import random
import sympy

from params import Params


class Chromosome(ABC):
    def __init__(self, params: Params, symbols: list[sympy.Symbol], genes: list[float]):
        self.params = params

        if len(symbols) <= 0 or len(symbols) > 2:
            raise ValueError("Symbols must be a list of length 1 or 2")

        self.symbols = symbols
        self.genes = list(
            map(lambda g: min(max(g, -self.params.DEPTH), self.params.DEPTH), genes)
        )

    def __str__(self):
        return f"Chromosome: {self.genes}"

    @staticmethod
    def random(
        params: Params, symbols: list[sympy.Symbol], sigma: float
    ) -> "Chromosome":
        genes = [random.gauss(0, sigma) for _ in symbols]
        return Chromosome(params, symbols, genes)

    def fitness(self, f: sympy.Expr) -> float:
        subs_map = {s: g for s, g in zip(self.symbols, self.genes)}

        return f.subs(subs_map).evalf()

    def crossover(self, other: "Chromosome") -> "Chromosome":
        if len(self.symbols) != len(other.symbols):
            raise ValueError("Symbols must be the same length")

        new_genes: list[float] = []

        if len(self.symbols) == 1:
            new_genes = [(self.genes[0] + other.genes[0]) / 2]
            return Chromosome(self.params, self.symbols, new_genes)

        new_genes = [self.genes[0], other.genes[1]]
        return Chromosome(self.params, self.symbols, new_genes)

    def mutate(self, sigma: float) -> "Chromosome":
        new_genes: list[float] = list(
            map(lambda g: g + random.gauss(0, sigma), self.genes)
        )

        return Chromosome(self.params, self.symbols, new_genes)
