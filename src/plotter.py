'''graphical interface'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation

from chromosome import Chromosome
from genetic import Genetic
from params import Params

matplotlib.use("TkAgg")


class Plotter:
    '''graphical interface'''
    _sc: plt.scatter

    def __init__(self, alg: Genetic, params: Params, is_2d: bool):
        self.alg = alg
        self.params = params
        self.is_2d = is_2d
        self._ax = None

    def show(self):
        '''shows a Cartesian plane with the function and representation of the individuals'''
        fig, ax = self._get_fig()
        self._ax = ax

        if self.params.AUTO_FIT:
            ax.set_aspect("auto")
        else:
            ax.set_aspect("equal", adjustable="datalim")

        ax.set_title(f"Animação de pontos sobre {self.alg.expr}")

        _ = animation.FuncAnimation(
            fig,
            self.update,
            frames=self.params.FPS,
            interval=1000 / self.params.FPS,
            blit=False,
        )

        plt.show()

    def _get_fig(self):
        if self.is_2d:
            return self._get_fig2d()
        return self._get_fig1d()

    def _get_fig2d(self):
        x_aux = np.linspace(-self.params.DEPTH, self.params.DEPTH, 25)
        y_aux = np.linspace(-self.params.DEPTH, self.params.DEPTH, 25)
        x, y = np.meshgrid(x_aux, y_aux)
        points = np.c_[x.ravel(), y.ravel()]
        z_flat = self.alg.batch_fitness(points)

        z = np.array(z_flat, dtype=np.float64).reshape(x.shape)

        fig, ax = plt.subplots(figsize=(8, 8))
        contour = ax.contourf(x, y, z, levels=self.params.PLOT_LEVELS_2D, cmap="viridis")
        ax.contour(x, y, z, levels=self.params.PLOT_LEVELS_2D, colors="black", linewidths=0.5)
        plt.colorbar(contour, ax=ax)

        self._sc = ax.scatter([], [], c="red", s=20, alpha=0.8)

        return fig, ax

    def _get_fig1d(self):
        x = np.linspace(-self.params.DEPTH, self.params.DEPTH, 100)
        y = self.alg.batch_fitness([[e] for e in x])

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x, y)
        self._sc = ax.scatter([], [], c="red", s=20, alpha=0.8)

        return fig, ax

    def update(self, _):
        """update the plot"""
        pop = self.alg.next_generation()
        self._scatter_pop(pop)

    def _scatter_pop(self, pop: list[Chromosome]):
        def get_x_and_y(c: Chromosome):
            if self.is_2d:
                return c.genes[0], c.genes[1]
            return c.genes[0], c.fitness(self.alg.expr)

        points = list(map(get_x_and_y, pop))
        self._sc.set_offsets(np.array(points))
