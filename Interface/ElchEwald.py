from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from Interface.ElchEwaldControl import ElchEwaldControl
from Interface.ElchEwaldPlot import ElchEwaldplot


class ElchEwald(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plot_frame = ElchEwaldplot()
        self.control_frame = ElchEwaldControl()

        vbox = QVBoxLayout()
        vbox.addWidget(self.plot_frame)
        vbox.addWidget(self.control_frame)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(20)

        self.setLayout(vbox)
