import matplotlib.font_manager as fm
import matplotlib.style
import matplotlib.ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class ElchPlot(FigureCanvasQTAgg):
    def __init__(self, figsize):
        matplotlib.style.use('Interface/Styles/elchi_dark.mplstyle')
        super().__init__(Figure(figsize=figsize))

        self.ax = ax = self.figure.subplots()

        self.toolbar = NavigationToolbar2QT(self, self)
        self.toolbar.hide()

        ax.set_xlabel('', fontproperties=fm.FontProperties(fname='Interface/Fonts/Roboto-Regular.ttf', size=14))
        ax.set_ylabel('', fontproperties=fm.FontProperties(fname='Interface/Fonts/Roboto-Regular.ttf', size=14))

        # First set the tick locations to defined values to be able to specify labels directly, which is necessary to
        # set the font via a path to the font file. Then switch back to auto locator.
        ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([0, 1]))
        ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator([0, 1]))
        ax.set_xticklabels([0, 1], fontproperties=fm.FontProperties(fname='Interface/Fonts/Roboto-Light.ttf', size=11))
        ax.set_yticklabels([0, 1], fontproperties=fm.FontProperties(fname='Interface/Fonts/Roboto-Light.ttf', size=11))
        ax.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
        ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
        ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

        self.figure.tight_layout()
