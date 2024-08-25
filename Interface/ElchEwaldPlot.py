import numpy as np

from Interface.ElchPlot import ElchPlot
from Signals.Signals import signals_engine


class ElchEwaldplot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(8, 8))

        self.k = 2 * np.pi / 1.5405980
        self.b = 2 * np.pi / 3.904

        self.spheres = {}
        self.arrows = {}

        self.plot_lattice()
        self.ax.set_aspect('equal')

        signals_engine.ewald.connect(self.plot)

    def plot_lattice(self):
        positions = np.meshgrid(np.arange(-4, 5) * self.b, np.arange(0, 5) * self.b)
        self.ax.plot(positions[0], positions[1], 'o', color='#7b8ccb')

    def plot_ewald_spheres(self, data):
        for sphere in self.spheres.values():
            sphere.remove()
        self.spheres[1], = self.ax.plot(data['large_ewald_x'], data['large_ewald_y'], '-', color='#7b8ccb', lw=1)
        self.spheres[2], = self.ax.plot(data['small_ewald_x_l'], data['small_ewald_y'], '--', color='#7b8ccb', lw=1)
        self.spheres[3], = self.ax.plot(data['small_ewald_x_r'], data['small_ewald_y'], '--', color='#7b8ccb', lw=1)
        self.figure.canvas.draw()

    def plot_vectors(self, data):
        for artist in self.arrows.values():
            artist.remove()

        self.arrows['in_1'] = self.ax.arrow(data['in_1'][0], data['in_1'][1], data['in_1'][2], data['in_1'][3],
                                            head_width=0.3, length_includes_head=True, lw=2, color='#86f8ab',
                                            overhang=0.5, zorder=5, head_length=0.3)
        self.arrows['in_2'] = self.ax.arrow(data['in_2'][0], data['in_2'][1], data['in_2'][2], data['in_2'][3],
                                            head_width=0.3, length_includes_head=True, lw=2, color='#86f8ab',
                                            overhang=0.5, zorder=5, head_length=0.3)
        self.arrows['out_1'] = self.ax.arrow(data['out_1'][0], data['out_1'][1], data['out_1'][2], data['out_1'][3],
                                             head_width=0.3, length_includes_head=True, lw=2, color='#f488f9',
                                             overhang=0.5, zorder=5, head_length=0.3)
        self.arrows['out_2'] = self.ax.arrow(data['out_2'][0], data['out_2'][1], data['out_2'][2], data['out_2'][3],
                                             head_width=0.3, length_includes_head=True, lw=2, color='#f488f9',
                                             overhang=0.5, zorder=5, head_length=0.3)
        self.arrows['scatter'] = self.ax.arrow(data['q'][0], data['q'][1], data['q'][2], data['q'][3], head_width=0.3,
                                               length_includes_head=True, lw=2, color='#faf0b1', overhang=0.5, zorder=5,
                                               head_length=0.3)

        self.figure.canvas.draw()

    def plot(self, data):
        self.plot_ewald_spheres(data['ewald'])
        self.plot_vectors(data['vectors'])
