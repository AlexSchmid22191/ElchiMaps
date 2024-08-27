from inspect import stack

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizeGrip, QStackedLayout

from Interface.ElchEwald import ElchEwald
from Interface.ElchRSM import ElchRSM
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

        self.rsm = ElchRSM()
        self.titlebar = ElchTitlebar()
        self.ribbon = ElchRibbon(menus=['RSM', 'ESV'])
        self.ewald = ElchEwald()

        panel_spacing = 20

        self.stackbox = QStackedLayout()
        self.stackbox.addWidget(self.rsm)
        self.stackbox.addWidget(self.ewald)

        vbox_inner = QVBoxLayout()
        vbox_inner.addLayout(self.stackbox)
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

        self.setLayout(hbox_outer)

        self.ribbon.buttongroup.buttonClicked.connect(self.adjust_visibility)
        self.ribbon.menu_buttons['RSM'].setChecked(True)

        self.show()

    def adjust_visibility(self, button):
        match button.objectName():
            case 'ESV':
                self.stackbox.setCurrentIndex(1)
            case 'RSM':
                self.stackbox.setCurrentIndex(0)
