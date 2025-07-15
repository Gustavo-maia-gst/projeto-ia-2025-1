import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from chromosome import Chromosome
from genetic import Genetic
from params import Params

matplotlib.use("TkAgg")


class Plotter:
    _sc: plt.scatter

    def __init__(self, alg: Genetic, params: Params, is_2d: bool):
        self.alg = alg
        self.params = params
        self.is_2d = is_2d

    def show(self):
        fig, ax = self._getFig()
        self._ax = ax

        if self.params.AUTO_FIT:
            ax.set_aspect("auto")
        else:
            ax.set_aspect("equal", adjustable="datalim")

        ax.set_title(f"Animação de pontos sobre {self.alg.expr}")

        ani = animation.FuncAnimation(
            fig,
            self._update,
            frames=self.params.FPS,
            interval=1000 / self.params.FPS,
            blit=False,
        )

        plt.show()

    def _getFig(self):
        if self.is_2d:
            return self._getFig2d()
        else:
            return self._getFig1d()

    def _getFig2d(self):
        x = np.linspace(-self.params.DEPTH, self.params.DEPTH, 25)
        y = np.linspace(-self.params.DEPTH, self.params.DEPTH, 25)
        X, Y = np.meshgrid(x, y)
        points = np.c_[X.ravel(), Y.ravel()]
        Z_flat = self.alg.batch_fitness(points)

        Z = np.array(Z_flat, dtype=np.float64).reshape(X.shape)

        fig, ax = plt.subplots(figsize=(8, 8))
        contour = ax.contourf(X, Y, Z, levels=self.params.PLOT_LEVELS_2D, cmap="viridis")
        ax.contour(X, Y, Z, levels=self.params.PLOT_LEVELS_2D, colors="black", linewidths=0.5)
        plt.colorbar(contour, ax=ax)

        self._sc = ax.scatter([], [], c="red", s=20, alpha=0.8)

        return fig, ax

    def _getFig1d(self):
        x = np.linspace(-self.params.DEPTH, self.params.DEPTH, 100)
        y = self.alg.batch_fitness([[e] for e in x])

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x, y)
        self._sc = ax.scatter([], [], c="red", s=20, alpha=0.8)

        return fig, ax

    def _update(self, frame):
        pop = self.alg.next_generation()
        self._scatter_pop(pop)

    def _scatter_pop(self, pop: list[Chromosome]):
        def get_x_and_y(c: Chromosome):
            if self.is_2d:
                return c.genes[0], c.genes[1]
            else:
                return c.genes[0], c.fitness(self.alg.expr)

        points = list(map(get_x_and_y, pop))
        self._sc.set_offsets(np.array(points))
