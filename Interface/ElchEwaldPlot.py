import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend_handler import HandlerPatch

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
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-5, 15)

        self.ax.set_axis_off()
        self.ax.hlines(0, -14.5, 14.5, color='#7b8ccb', lw=2)
        self.ax.vlines(0, 0, 14.5, color='#7b8ccb', lw=2)

        self.ax.add_patch(plt.Polygon([[0, 15], [-0.25, 14.5], [0.25, 14.5]], color='#7b8ccb'))
        self.ax.add_patch(plt.Polygon([[15, 0], [14.5, -0.25], [14.5, 0.25]], color='#7b8ccb'))

        self.ax.text(14, -1, r'$q_{\parallel}$',
                     fontproperties=fm.FontProperties(fname='Interface/Fonts/Roboto-Regular.ttf', size=14))
        self.ax.text(0.5, 14.5, r'$q_{\perp}$',
                     fontproperties=fm.FontProperties(fname='Interface/Fonts/Roboto-Regular.ttf', size=14))

        handles = [
            mpatches.FancyArrow(0, 0, 0, 0, head_width=0.3, length_includes_head=True, lw=2, color=color, overhang=0.5,
                                zorder=5, head_length=0.3) for color in ['#86f8ab', '#faf0b1', '#f488f9']]
        handles += [mlines.Line2D([], [], ls=ls, color='#7b8ccb', lw=1) for ls in ['-', '--']]
        labels = [r'Incoming wave vector $q_{\mathrm{in}}$', r'Outgoing wave vector $q_{\mathrm{out}}$',
                  r'Scattering vector $q$', 'Limited by wavelength', 'Limited by reflection/transmission']
        self.ax.legend(handles, labels, handler_map={mpatches.FancyArrow: HandlerArrow()}, frameon=False, ncol=2,
                       prop=fm.FontProperties(fname='Interface/Fonts/Roboto-Regular.ttf', size=14), loc=(0, -0.15))
        signals_engine.ewald.connect(self.plot)

    def plot_lattice(self):
        positions = np.meshgrid(np.arange(-8, 9) * self.b, np.arange(0, 9) * self.b)
        self.ax.plot(positions[0], positions[1], 'o', color='#7b8ccb')
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-5, 15)

    def plot_ewald_spheres(self, data):
        for sphere in self.spheres.values():
            sphere.remove()
        self.spheres[1], = self.ax.plot(data['large_ewald_x'], data['large_ewald_y'], '-', color='#7b8ccb', lw=1)
        self.spheres[2], = self.ax.plot(data['small_ewald_x_l'], data['small_ewald_y'], '--', color='#7b8ccb', lw=1)
        self.spheres[3], = self.ax.plot(data['small_ewald_x_r'], data['small_ewald_y'], '--', color='#7b8ccb', lw=1)
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-5, 15)
        self.figure.canvas.draw()

    def plot_vectors(self, data):
        for artist in self.arrows.values():
            artist.remove()

        self.arrows['in_1'] = self.ax.arrow(data['in_1'][0], data['in_1'][1], data['in_1'][2], data['in_1'][3],
                                            head_width=0.3, length_includes_head=True, lw=2, color='#86f8ab',
                                            overhang=0.5, zorder=5, head_length=0.3,
                                            label=r'Incoming wave vector $q_{\mathrm{in}}$')
        self.arrows['in_2'] = self.ax.arrow(data['in_2'][0], data['in_2'][1], data['in_2'][2], data['in_2'][3],
                                            head_width=0.3, length_includes_head=True, lw=2, color='#86f8ab',
                                            overhang=0.5, zorder=5, head_length=0.3)
        self.arrows['out_1'] = self.ax.arrow(data['out_1'][0], data['out_1'][1], data['out_1'][2], data['out_1'][3],
                                             head_width=0.3, length_includes_head=True, lw=2, color='#f488f9',
                                             overhang=0.5, zorder=5, head_length=0.3,
                                             label=r'Diffracted wave vector $q_{\mathrm{out}}$')
        self.arrows['out_2'] = self.ax.arrow(data['out_2'][0], data['out_2'][1], data['out_2'][2], data['out_2'][3],
                                             head_width=0.3, length_includes_head=True, lw=2, color='#f488f9',
                                             overhang=0.5, zorder=5, head_length=0.3)
        self.arrows['scatter'] = self.ax.arrow(data['q'][0], data['q'][1], data['q'][2], data['q'][3], head_width=0.3,
                                               length_includes_head=True, lw=2, color='#faf0b1', overhang=0.5, zorder=5,
                                               head_length=0.3, label=r'Scattering vector $q$')
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-5, 15)

        self.figure.canvas.draw()

    def plot(self, data):
        self.plot_ewald_spheres(data['ewald'])
        self.plot_vectors(data['vectors'])


class HandlerArrow(HandlerPatch):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        p = mpatches.FancyArrow(0, 0.5 * height, width, 0, length_includes_head=True, head_width=0.75 * height)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]
