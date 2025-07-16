"""
This class contains the hyperparameters for the genetic algorithm.

It also contains some default values that may be overwritten by the user via
command line arguments or via a config file.

A brief description of the selection methods:

    Elitism: The elitism rate selects the best chromosomes to go to the next generation.

    Tournament: TOURNAMENT_RATE chromosomes are chosen by tournaments of size TOURNAMENT_SIZE,
                the best one gets mutated and goes to the next generation.

    Crossover: CROSSOVER_RATE of the chromosomes are chosen by crossover,
               two chromossomes are selected and crossed, the child gets mutated and goes 
               to the next generation,
               crossover is applied to the chromosomes using the tournament method.

    Random: RANDOM_RATE of the chromosomes are randommically generated to go to the next generation.

    Lottery: 1 - TOURNAMENT_RATE - ELITISM_RATE - CROSSOVER_RATE - RANDOM_RATE of the chromosomes
                 are chosen by lottery, the lucky one goes to the next generation,
"""


class Params:
    """Default values as constants"""

    DEFAULT_MAX_STEPS: int = 1000
    DEFAULT_POPULATION_SIZE: int = 32
    DEFAULT_STEP_SIZE: float = 1
    DEFAULT_TOURNAMENT_RATE: float = 0.4
    DEFAULT_TOURNAMENT_SIZE: int = 4
    DEFAULT_ELITISM_RATE: float = 0.1
    DEFAULT_CROSSOVER_RATE: float = 0.3
    DEFAULT_CROSSOVER_MUTATION_RATE: float = 0.05
    DEFAULT_LOTTERY_RATE: float = 0.1
    DEFAULT_RANDOM_RATE: float = 0.1

    DEFAULT_FPS: int = 5
    DEFAULT_DEPTH: int = 50
    DEFAULT_PLOT_LEVELS_2D: int = 35
    DEFAULT_AUTO_FIT: bool = False

    # Class attributes using default constants
    POPULATION_SIZE: int = (
        DEFAULT_POPULATION_SIZE  # Number of chromosomes in the population
    )
    MAX_STEPS: int = DEFAULT_MAX_STEPS  # Maximum number of steps
    STEP_SIZE: float = DEFAULT_STEP_SIZE  # Mutation rate of the chromosomes

    TOURNAMENT_RATE: float = (
        DEFAULT_TOURNAMENT_RATE  # Rate of the next generation choosen by tournament
    )
    TOURNAMENT_SIZE: int = (
        DEFAULT_TOURNAMENT_SIZE  # Number of chromosomes in the tournament
    )

    ELITISM_RATE: float = (
        DEFAULT_ELITISM_RATE  # Rate of the next generation choosen by elitism
    )

    CROSSOVER_RATE: float = (
        DEFAULT_CROSSOVER_RATE  # Rate of the next generation choosen by crossover
    )
    CROSSOVER_MUTATION_RATE: float = (
        DEFAULT_CROSSOVER_MUTATION_RATE  # Mutation rate applied to chromosomes after crossover
    )

    LOTTERY_RATE: float = (
        DEFAULT_LOTTERY_RATE  # Rate of the next generation choosen by lottery
    )

    RANDOM_RATE: float = (
        DEFAULT_RANDOM_RATE  # Rate of the next generation choosen by random
    )

    FPS: int = DEFAULT_FPS  # Frames per second
    DEPTH: int = DEFAULT_DEPTH  # Depth of the plot
    PLOT_LEVELS_2D: int = DEFAULT_PLOT_LEVELS_2D  # Number of levels in the 2D plot
    AUTO_FIT: bool = DEFAULT_AUTO_FIT  # Whether to auto fit the plot
