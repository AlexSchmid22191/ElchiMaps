from lib2to3.fixes.fix_metaclass import remove_trailing_newline

from Interface.ElchPlot import ElchPlot
from Signals.Signals import signals_engine
import matplotlib.ticker as mpt


class ElchLinePlot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(6, 3))

        self.coordinates = 'Angles'
        self.scale = 'linear'
        self.line, = self.ax.plot([1], [1])
        signals_engine.line_scan_1D.connect(self.plot_line)
        self.ax.set_ylabel('Intensity (a.u.)')

        self.ax.yaxis.set_major_formatter(mpt.FuncFormatter(self.fancy_sci_formatter))
        self.ax.set_xlim(1, 100)
        self.autoscale()

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
                    self.ax.set_xlabel(r'$\mathrm{Scattering\ angle}\ (\mathrm{\degree})$')

        self.autoscale()

    @staticmethod
    def fancy_sci_formatter(number, *args):
        e_string = f'{number:.1e}'
        coeff, expo = e_string.split('e')
        expo = int(expo)
        return fr'${coeff}\cdot 10^{expo}$'

    def set_norm(self, norm):
        match norm.objectName():
            case 'Linear':
                self.ax.set_yscale('linear')
            case 'Logarithmic':
                self.ax.set_yscale('log')
            case 'Square Root':
                self.ax.set_yscale('function', functions=(lambda x: x**0.5, lambda x: x**2))
        self.autoscale()

