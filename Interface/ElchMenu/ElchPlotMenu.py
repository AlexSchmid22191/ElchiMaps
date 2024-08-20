from PySide6.QtWidgets import QWidget, QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout, QAbstractButton


class ElchPlotMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons = {key: QPushButton(parent=self, text=key, objectName=key) for key in ['Autoscale', 'Zoom']}
        self.buttons['Zoom'].setCheckable(True)

        self.coordinate_checks = {key: QRadioButton(parent=self, text=key, objectName=key)
                                  for key in ['Angles', 'Reciprocal Vectors']}
        self.coordinate_check_group = QButtonGroup()
        self.coordinate_check_group.setExclusive(True)
        self.coordinate_checks['Angles'].setChecked(True)

        self.line_checks = {key: QRadioButton(parent=self, text=key, objectName=key)
                            for key in ['Omega', '2 Theta', 'Radial', 'q parallel', 'q normal']}
        self.line_check_group = QButtonGroup()
        self.line_check_group.setExclusive(True)

        self.line_position_box = QDoubleSpinBox(decimals=2, singleStep=1e-2, minimum=0, maximum=90, suffix=u'°')

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(text='Coordinate System', objectName='Header'))
        for key, button in self.coordinate_checks.items():
            self.coordinate_check_group.addButton(button)
            vbox.addWidget(button)
        vbox.addSpacing(20)

        vbox.addWidget(QLabel(text='Line Scans', objectName='Header'))
        for key, button in self.line_checks.items():
            self.line_check_group.addButton(button)
            vbox.addWidget(button)
        vbox.addSpacing(10)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(text='Line scan position:'))
        hbox.addWidget(self.line_position_box)
        vbox.addLayout(hbox)

        vbox.addSpacing(20)

        vbox.addWidget(QLabel(text='Plotting Control', objectName='Header'))
        for button in self.buttons.values():
            vbox.addWidget(button)

        vbox.addStretch()
        vbox.setSpacing(10)
        vbox.setContentsMargins(10, 10, 10, 10)
        self.setLayout(vbox)

        self.coordinate_check_group.buttonClicked.connect(self.change_coordinates)

    def change_coordinates(self, button):
        match button.objectName():
            case 'Angles':
                self.line_position_box.setSuffix('°')
                # Send a signal to the plot wondows to change units and map
            case 'Reciprocal Vectors':
                self.line_position_box.setSuffix(u' Å⁻¹')
                # Send a signal to the plot wondows to change units and map
