from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from Interface.ElchMenu.ElchFileMenu import ElchFileMenu
from Interface.ElchMenu.ElchPlotMenu import ElchPlotMenu


class ElchMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(260)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.menus = {'File': ElchFileMenu(), 'Plotting': ElchPlotMenu()}

        vbox = QVBoxLayout()
        for menu in self.menus:
            self.menus[menu].setVisible(False)
            vbox.addWidget(self.menus[menu])
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vbox)

    def adjust_visibility(self, button, visibility):
        menu = button.objectName()
        self.menus[menu].setVisible(visibility)
