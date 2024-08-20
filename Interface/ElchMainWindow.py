from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizeGrip

from Interface.ElchContourPlot import ElchContourPlot
from Interface.ElchLinePlot import ElchLinePlot
from Interface.ElchMenu.ElchMenu import ElchMenu
from Interface.ElchRibbon import ElchRibbon
from Interface.ElchTitleBar import ElchTitlebar


class ElchMainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowFlags(Qt.FramelessWindowHint)

        QFontDatabase.addApplicationFont('Fonts/Roboto-Light.ttf')
        QFontDatabase.addApplicationFont('Fonts/Roboto-Regular.ttf')

        with open('Interface/Styles/style.qss') as stylefile:
            self.setStyleSheet(stylefile.read())

        self.controlmenu = ElchMenu()
        self.titlebar = ElchTitlebar()
        self.lineframe = ElchLinePlot()
        self.contourframe = ElchContourPlot()
        self.ribbon = ElchRibbon(menus=self.controlmenu.menus)

        panel_spacing = 20

        vbox_innermost = QVBoxLayout()
        vbox_innermost.addWidget(self.contourframe, stretch=1)
        vbox_innermost.addWidget(self.lineframe, stretch=0.5)

        hbox_inner = QHBoxLayout()
        hbox_inner.addLayout(vbox_innermost)
        hbox_inner.addWidget(self.controlmenu, stretch=0)
        hbox_inner.setSpacing(panel_spacing)
        hbox_inner.setContentsMargins(0, 0, 0, 0)

        vbox_inner = QVBoxLayout()
        vbox_inner.addLayout(hbox_inner, stretch=1)
        # Here a statusbar could be added in the future
        vbox_inner.setSpacing(panel_spacing)
        vbox_inner.setContentsMargins(panel_spacing, panel_spacing, panel_spacing - 13, panel_spacing)

        sizegrip = QSizeGrip(self)
        hbox_mid = QHBoxLayout()
        hbox_mid.addLayout(vbox_inner, stretch=1)
        hbox_mid.addWidget(sizegrip, alignment=Qt.AlignBottom | Qt.AlignRight)
        hbox_mid.setContentsMargins(0, 0, 0, 0)
        hbox_mid.setSpacing(0)

        vbox_outer = QVBoxLayout()
        vbox_outer.addWidget(self.titlebar, stretch=0)
        vbox_outer.addLayout(hbox_mid, stretch=1)
        vbox_outer.setContentsMargins(0, 0, 0, 0)
        vbox_outer.setSpacing(0)

        hbox_outer = QHBoxLayout()
        hbox_outer.addWidget(self.ribbon, stretch=0)
        hbox_outer.addLayout(vbox_outer, stretch=1)
        hbox_outer.setContentsMargins(0, 0, 0, 0)
        hbox_outer.setSpacing(0)

        self.ribbon.buttongroup.buttonToggled.connect(self.controlmenu.adjust_visibility)
        self.ribbon.menu_buttons['File'].setChecked(True)

        self.setLayout(hbox_outer)
        self.show()
