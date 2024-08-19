from Interface.ElchPlot import ElchPlot


class ElchLinePlot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(6, 3))

        self.coordinates = 'Angles'
        self.line = None