# TODO: Make it great

import argparse
import os
import json

import sympy
from genetic import Genetic
from params import Params
from plotter import Plotter

CONFIG_FILE = "../config.json"


def define_params(args: argparse.ArgumentParser) -> Params:
    args.add_argument(
        "--population-size", type=int, default=Params.DEFAULT_POPULATION_SIZE
    )
    args.add_argument("--step-size", type=float, default=Params.DEFAULT_STEP_SIZE)
    args.add_argument(
        "--tournament-rate", type=float, default=Params.DEFAULT_TOURNAMENT_RATE
    )
    args.add_argument(
        "--tournament-size", type=int, default=Params.DEFAULT_TOURNAMENT_SIZE
    )
    args.add_argument("--elitism-rate", type=float, default=Params.DEFAULT_ELITISM_RATE)
    args.add_argument(
        "--crossover-rate", type=float, default=Params.DEFAULT_CROSSOVER_RATE
    )
    args.add_argument(
        "--crossover-mutation-rate",
        type=float,
        default=Params.DEFAULT_CROSSOVER_MUTATION_RATE,
    )
    args.add_argument("--lottery-rate", type=float, default=Params.DEFAULT_LOTTERY_RATE)
    args.add_argument("--fps", type=int, default=Params.DEFAULT_FPS)
    args.add_argument("-d", "--depth", type=int, default=Params.DEFAULT_DEPTH)
    args.add_argument(
        "--plot-levels", type=int, default=Params.DEFAULT_PLOT_LEVELS_2D
    )


def get_params(args: argparse.ArgumentParser) -> Params:
    parsed_args = args.parse_args()

    params = Params()

    params.POPULATION_SIZE = parsed_args.population_size
    params.STEP_SIZE = parsed_args.step_size
    params.TOURNAMENT_RATE = parsed_args.tournament_rate
    params.TOURNAMENT_SIZE = parsed_args.tournament_size
    params.ELITISM_RATE = parsed_args.elitism_rate
    params.CROSSOVER_RATE = parsed_args.crossover_rate
    params.CROSSOVER_MUTATION_RATE = parsed_args.crossover_mutation_rate
    params.LOTTERY_RATE = parsed_args.lottery_rate
    params.FPS = parsed_args.fps
    params.DEPTH = parsed_args.depth
    params.PLOT_LEVELS_2D = parsed_args.plot_levels

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)

                params.POPULATION_SIZE = config.get(
                    "population_size", params.POPULATION_SIZE
                )
                params.STEP_SIZE = config.get("step_size", params.STEP_SIZE)
                params.TOURNAMENT_RATE = config.get(
                    "tournament_rate", params.TOURNAMENT_RATE
                )
                params.TOURNAMENT_SIZE = config.get(
                    "tournament_size", params.TOURNAMENT_SIZE
                )
                params.ELITISM_RATE = config.get("elitism_rate", params.ELITISM_RATE)
                params.CROSSOVER_RATE = config.get(
                    "crossover_rate", params.CROSSOVER_RATE
                )
                params.CROSSOVER_MUTATION_RATE = config.get(
                    "crossover_mutation_rate", params.CROSSOVER_MUTATION_RATE
                )
                params.LOTTERY_RATE = config.get("lottery_rate", params.LOTTERY_RATE)
                params.FPS = config.get("fps", params.FPS)
                params.DEPTH = config.get("depth", params.DEPTH)

        except Exception as ex:
            print(f"Error loading config file: {ex}")

    return params


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Genetic Algorithm")
    define_params(args)
    params = get_params(args)

    funcionStr = input("Defina a função: ")

    try:
        expr = sympy.sympify(funcionStr)
    except Exception as ex:
        print(f"Função inválida.\n{ex}")
        exit(1)

    symbols = list(expr.free_symbols)
    alg = Genetic(params, symbols, expr)

    plotter = Plotter(alg, params, len(symbols) == 2)

    plotter.show()
