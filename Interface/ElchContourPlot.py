from Interface.ElchPlot import ElchPlot


class ElchContourPlot(ElchPlot):
    def __init__(self):
        super().__init__(figsize=(6, 6))

        self.coordinates = 'Angles'
        self.colormesh = None
