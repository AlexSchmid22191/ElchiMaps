from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizeGrip

from Interface.ElchContourPlot import ElchContourPlot
from Interface.ElchLinePlot import ElchLinePlot
from Interface.ElchMenu import ElchMenu
from Interface.ElchRibbon import ElchRibbon
from Interface.ElchTitleBar import ElchTitlebar
from Interface.ElchEwald import ElchEwald


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
        self.ribbon = ElchRibbon(menus=['RSM', 'ESV'])
        self.ewald = ElchEwald()
        self.ewald.setVisible(False)

        panel_spacing = 20

        vbox_innermost = QVBoxLayout()
        vbox_innermost.addWidget(self.contourframe, stretch=2)
        vbox_innermost.addWidget(self.lineframe, stretch=1)

        hbox_inner = QHBoxLayout()
        hbox_inner.addLayout(vbox_innermost, stretch=1)
        hbox_inner.addWidget(self.controlmenu, stretch=0)
        hbox_inner.setSpacing(panel_spacing)
        hbox_inner.setContentsMargins(0, 0, 0, 0)

        vbox_inner = QVBoxLayout()
        vbox_inner.addLayout(hbox_inner, stretch=1)
        vbox_inner.addWidget(self.ewald, stretch=1)
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

        self.ribbon.buttongroup.buttonClicked.connect(self.adjust_visibility)
        self.ribbon.menu_buttons['RSM'].setChecked(True)

        self.controlmenu.plot_buttons['Zoom'].toggled.connect(self.contourframe.toggle_zoom)
        self.controlmenu.plot_buttons['Autoscale'].clicked.connect(self.contourframe.autoscale)

        self.controlmenu.plot_buttons['Zoom'].toggled.connect(self.lineframe.toggle_zoom)
        self.controlmenu.plot_buttons['Autoscale'].clicked.connect(self.lineframe.autoscale)

        self.controlmenu.normalize_group.buttonClicked.connect(self.contourframe.set_norm)
        self.controlmenu.normalize_group.buttonClicked.connect(self.lineframe.set_norm)
        self.controlmenu.color_select.currentTextChanged.connect(self.contourframe.set_color)

        self.setLayout(hbox_outer)

        self.show()

    def adjust_visibility(self, button):
        match button.objectName():
            case 'ESV':
                self.contourframe.setVisible(False)
                self.lineframe.setVisible(False)
                self.controlmenu.setVisible(False)
                self.ewald.setVisible(True)
            case 'RSM':
                self.contourframe.setVisible(True)
                self.lineframe.setVisible(True)
                self.controlmenu.setVisible(True)
                self.ewald.setVisible(False)

