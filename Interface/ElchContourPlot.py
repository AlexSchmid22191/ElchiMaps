from Interface.ElchPlot import ElchPlot
from Signals.Signals import signals_engine


class ElchContourPlot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(6, 6))

        self.coordinates = 'Angles'
        self.colormesh = None

        signals_engine.map_data_angle.connect(self.plot_angle_map)

    def plot_angle_map(self, data):
        self.colormesh = self.ax.pcolormesh(data['om'], data['tt'], data['counts'], cmap='plasma')
        self.ax.set_xlabel(r'$\omega\ (\degree)$')
        self.ax.set_ylabel(r'$2\Theta\ (\degree)$')

        self.ax.autoscale()
        self.figure.tight_layout()
        self.figure.canvas.draw()
