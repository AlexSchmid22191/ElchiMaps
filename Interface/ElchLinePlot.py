from Interface.ElchPlot import ElchPlot
from Signals.Signals import signals_engine


class ElchLinePlot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(6, 3))

        self.coordinates = 'Angles'
        self.scale = 'linear'
        self.line = None
        signals_engine.line_scan_1D.connect(self.plot_line)
        self.ax.set_ylabel('Intensity (a.u.)')

    def plot_line(self, data):
        if all(value is not None for value in data.values()):
            if self.line is not None:
                self.line.remove()
            self.ax.relim()
            self.line, = self.ax.plot(data['x'], data['y'], '-', lw=1, color='#7b8ccb')

            match data['x_coord']:
                case 'q_parallel':
                    self.ax.set_xlabel(r'$q_{\parallel}\ (\mathrm{\AA^{-1}})$')
                case 'q_normal':
                    self.ax.set_xlabel(r'$q_{\perp}\ (\mathrm{\AA^{-1}})$')
                case 'omega':
                    self.ax.set_xlabel(r'$\omega\ (\mathrm{\degree})$')
                case '2theta':
                    self.ax.set_xlabel(r'$2 \Theta\ (\mathrm{\degree})$')
                case 'radial':
                    self.ax.set_xlabel(r'$\mathrm{Scattering angle}\ (\mathrm{\degree})$')

        self.autoscale()
