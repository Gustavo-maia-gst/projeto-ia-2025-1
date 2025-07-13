import random
import sympy
from chromosome import Chromosome
from params import Params


class Genetic:
    def __init__(self, params: Params, symbols: list[sympy.Symbol], expr: sympy.Expr):
        self.params = params
        self.symbols = symbols
        self.expr = expr

        self.__validate_params()

        self.population = [Chromosome.random(params, symbols, params.STEP_SIZE)]

    def next_generation(self) -> list[Chromosome]:
        if len(self.population) < self.params.POPULATION_SIZE:
            randomic = [
                Chromosome.random(self.params, self.symbols, self.params.DEFAULT_DEPTH)
                for _ in self.population
            ]
            self.population.extend(randomic)
            return self.population

        ordered = sorted(
            self.population, key=lambda c: c.fitness(self.expr), reverse=True
        )

        new_generation = []

        new_generation.extend(self.get_elitism_pop(ordered))
        new_generation.extend(self.get_tournament_pop(ordered))
        new_generation.extend(self.get_crossover_pop(ordered))
        new_generation.extend(self.get_random_pop(ordered))

        while len(new_generation) < self.params.POPULATION_SIZE:
            lucky_one = random.randint(0, len(ordered) - 1)
            new_generation.append(ordered[lucky_one].mutate(self.params.STEP_SIZE))

        self.population = new_generation

        return self.population

    def get_elitism_pop(self, ordered: list[Chromosome]) -> list[Chromosome]:
        return ordered[: int(self.params.ELITISM_RATE * len(ordered))]

    def get_tournament_pop(self, ordered: list[Chromosome]) -> list[Chromosome]:
        tournament_pop_size = int(self.params.TOURNAMENT_RATE * len(ordered))

        return [
            self.__tournament(ordered).mutate(self.params.STEP_SIZE)
            for _ in range(tournament_pop_size)
        ]

    def get_random_pop(self, ordered: list[Chromosome]) -> list[Chromosome]:
        random_pop_size = int(self.params.RANDOM_RATE * len(ordered))

        return [
            Chromosome.random(self.params, self.symbols, self.params.DEFAULT_DEPTH)
            for _ in range(random_pop_size)
        ]

    def get_crossover_pop(self, ordered: list[Chromosome]) -> list[Chromosome]:
        crossover_pop_size = int(self.params.CROSSOVER_RATE * len(ordered))
        crossover_pop = []
        for _ in range(crossover_pop_size):
            parent1 = self.__tournament(ordered)
            parent2 = self.__tournament(ordered)

            crossover_pop.append(
                parent1.crossover(parent2).mutate(self.params.CROSSOVER_MUTATION_RATE)
            )

        return crossover_pop

    def __tournament(self, ordered: list[Chromosome]) -> Chromosome:
        participants = [
            random.randint(0, len(ordered) - 1)
            for _ in range(self.params.TOURNAMENT_SIZE)
        ]

        return ordered[min(participants)]

    def batchFitness(self, genes: list[list[float]]) -> list[float]:
        if any(len(gene) != len(self.symbols) for gene in genes):
            raise ValueError(
                "All genes must have the same length as the number of symbols"
            )

        def evaluate(gene: list[float]) -> float:
            subs = {self.symbols[i]: gene[i] for i in range(len(self.symbols))}
            return self.expr.subs(subs).evalf()

        return [evaluate(gene) for gene in genes]

    def __validate_params(self):
        rates = [
            self.params.ELITISM_RATE,
            self.params.TOURNAMENT_RATE,
            self.params.CROSSOVER_RATE,
            self.params.LOTTERY_RATE,
        ]

        if not is_power_of_two(self.params.POPULATION_SIZE):
            raise ValueError("Population size must be a power of 2")

        if any(rate < 0 for rate in rates):
            raise ValueError("Rates must be positive")

        if sum(rates) > 1:
            raise ValueError("The sum of the rates must not be 1")

        if (
            self.params.TOURNAMENT_SIZE < 1
            or self.params.TOURNAMENT_SIZE > self.params.POPULATION_SIZE
        ):
            raise ValueError(
                "Tamanho do torneio deve ser entre 1 e o tamanho da população"
            )


def is_power_of_two(n: int) -> bool:
    return (n & (n - 1)) == 0
