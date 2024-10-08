import matplotlib.colors

from Interface.ElchPlot import ElchPlot
from Signals.Signals import signals_engine, signals_gui


class ElchContourPlot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(6, 6))

        self.coordinates = 'Angles'
        self.norm = 'linear'
        self.color = 'magma'
        self.colormesh = None
        self.line, = self.ax.plot([], [], '-', lw=1, color='#7b8ccb')

        signals_engine.map_data_angle.connect(self.plot_angle_map)
        signals_engine.map_data_q.connect(self.plot_q_map)
        signals_engine.line_Scan_2D.connect(self.plot_line_cut)
        signals_gui.export_images.connect(self.save)

    def plot_angle_map(self, data):
        self.coordinates = 'Angles'
        if all(value is not None for value in data.values()):
            if self.colormesh is not None:
                self.colormesh.remove()
            if self.line is not None:
                self.line.set_data([], [])
            self.ax.relim()
            self.colormesh = self.ax.pcolormesh(data['om'], data['tt'], data['counts'], cmap=self.color, norm=self.norm)
        self.ax.set_xlabel(r'$\omega\ (\degree)$')
        self.ax.set_ylabel(r'$2\Theta\ (\degree)$')
        self.autoscale()

    def plot_q_map(self, data):
        self.coordinates = 'Reciprocal'
        if all(value is not None for value in data.values()):
            if self.colormesh is not None:
                self.colormesh.remove()
            if self.line is not None:
                self.line.set_data([], [])
            self.ax.relim()
            self.colormesh = self.ax.pcolormesh(data['q_para'], data['q_norm'], data['q_counts'], cmap=self.color,
                                                norm=self.norm)
        self.ax.set_xlabel(r'$q_{\parallel}\ (\mathrm{\AA^{-1}})$')
        self.ax.set_ylabel(r'$q_{\perp}\ (\mathrm{\AA^{-1}})$')
        self.autoscale()

    def set_norm(self, norm):
        match norm.objectName():
            case 'Linear':
                self.norm = 'linear'
            case 'Logarithmic':
                self.norm = 'log'
            case 'Square Root':
                self.norm = matplotlib.colors.PowerNorm(0.5)

        match self.coordinates:
            case 'Angles':
                signals_gui.get_angle_map.emit()
            case 'Reciprocal':
                signals_gui.get_q_map.emit()

    def set_color(self, color):
        self.color = color
        match self.coordinates:
            case 'Angles':
                signals_gui.get_angle_map.emit()
            case 'Reciprocal':
                signals_gui.get_q_map.emit()

    def plot_line_cut(self, data):
        if all(value is not None for value in data.values()):
            if self.line is not None:
                self.line.set_data(data['x'], data['y'])
            self.draw()

    def save(self, save_details):
        if save_details.get('option') == '2D Map - Image':
            self.figure.savefig(fname=save_details.get('file_path'), format='png', dpi=600)
