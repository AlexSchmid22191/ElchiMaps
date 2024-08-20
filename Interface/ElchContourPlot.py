from Interface.ElchPlot import ElchPlot
from Signals.Signals import signals_engine


class ElchContourPlot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(6, 6))

        self.coordinates = 'Angles'
        self.colormesh = None

        signals_engine.map_data_angle.connect(self.plot_angle_map)
        signals_engine.map_data_q.connect(self.plot_q_map)

    def plot_angle_map(self, data):
        if all(value is not None for value in data.values()):
            if self.colormesh is not None:
                self.colormesh.remove()
            self.ax.relim()
            self.colormesh = self.ax.pcolormesh(data['om'], data['tt'], data['counts'], cmap='plasma', norm='log')
        self.ax.set_xlabel(r'$\omega\ (\degree)$')
        self.ax.set_ylabel(r'$2\Theta\ (\degree)$')
        self.autoscale()

    def plot_q_map(self, data):
        if all(value is not None for value in data.values()):
            if self.colormesh is not None:
                self.colormesh.remove()
            self.ax.relim()
            self.colormesh = self.ax.pcolormesh(data['q_para'], data['q_norm'], data['q_counts'], cmap='plasma', norm='log')
        self.ax.set_xlabel(r'$q_{\parallel}\ (\mathrm{\AA^{-1}})$')
        self.ax.set_ylabel(r'$q_{\perp}\ (\mathrm{\AA^{-1}})$')
        self.autoscale()