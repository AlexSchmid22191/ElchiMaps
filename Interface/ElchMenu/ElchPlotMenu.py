from PySide6.QtWidgets import QWidget, QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QLabel


class ElchPlotMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons = {key: QPushButton(parent=self, text=key, objectName=key) for key in ['Autoscale', 'Zoom']}
        self.buttons['Zoom'].setCheckable(True)

        self.coordinate_checks = {key: QRadioButton(parent=self, text=key, objectName=key)
                                  for key in ['Angles', 'Reciprocal Vectors']}
        self.coordinate_check_group = QButtonGroup()
        self.coordinate_check_group.setExclusive(True)

        self.line_checkcs = {key: QRadioButton(parent=self, text=key, objectName=key)
                             for key in ['Omega', '2 Theta', 'q parallel', 'q normal']}
        self.line_check_group = QButtonGroup()
        self.line_check_group.setExclusive(True)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(text='Coordinate System', objectName='Header'))
        for key, button in self.coordinate_checks.items():
            self.coordinate_check_group.addButton(button)
            vbox.addWidget(button)
        vbox.addSpacing(20)

        vbox.addWidget(QLabel(text='Line Scans', objectName='Header'))
        for key, button in self.line_checkcs.items():
            self.line_check_group.addButton(button)
            vbox.addWidget(button)
        vbox.addSpacing(20)

        vbox.addWidget(QLabel(text='Plotting Control', objectName='Header'))
        for button in self.buttons.values():
            vbox.addWidget(button)

        vbox.addStretch()
        vbox.setSpacing(10)
        vbox.setContentsMargins(10, 10, 10, 10)
        self.setLayout(vbox)
