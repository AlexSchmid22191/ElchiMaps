from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget

from Interface.ElchContourPlot import ElchContourPlot
from Interface.ElchLinePlot import ElchLinePlot
from Interface.ElchMenu import ElchMenu


class ElchRSM(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controlmenu = ElchMenu()
        self.lineframe = ElchLinePlot()
        self.contourframe = ElchContourPlot()

        panel_spacing = 20

        vbox = QVBoxLayout()
        vbox.addWidget(self.contourframe, stretch=2)
        vbox.addWidget(self.lineframe, stretch=1)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox, stretch=1)
        hbox.addWidget(self.controlmenu, stretch=0)
        hbox.setSpacing(panel_spacing)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.controlmenu.plot_buttons['Zoom'].toggled.connect(self.contourframe.toggle_zoom)
        self.controlmenu.plot_buttons['Autoscale'].clicked.connect(self.contourframe.autoscale)

        self.controlmenu.plot_buttons['Zoom'].toggled.connect(self.lineframe.toggle_zoom)
        self.controlmenu.plot_buttons['Autoscale'].clicked.connect(self.lineframe.autoscale)

        self.controlmenu.normalize_group.buttonClicked.connect(self.contourframe.set_norm)
        self.controlmenu.normalize_group.buttonClicked.connect(self.lineframe.set_norm)
        self.controlmenu.color_select.currentTextChanged.connect(self.contourframe.set_color)

        self.setLayout(hbox)
