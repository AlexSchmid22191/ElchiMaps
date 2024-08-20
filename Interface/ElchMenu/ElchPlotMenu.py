from PySide6.QtWidgets import QWidget, QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QLabel, QDoubleSpinBox, \
    QHBoxLayout
from Signals.Signals import signals_gui

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

        self.para_box_label = QLabel(text='Omega')
        self.norm_box_label = QLabel(text='2 Theta')
        self.line_box_para = QDoubleSpinBox(decimals=2, singleStep=1e-2, minimum=0, maximum=90, suffix=u'°')
        self.line_box_norm = QDoubleSpinBox(decimals=2, singleStep=1e-2, minimum=0, maximum=90, suffix=u'°')

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
        hbox.addWidget(self.para_box_label)
        hbox.addWidget(self.line_box_para)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.norm_box_label)
        hbox.addWidget(self.line_box_norm)
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
        signals_gui.load_file.connect(lambda: self.coordinate_checks['Angles'].setChecked(True))

    def change_coordinates(self, button):
        match button.objectName():
            case 'Angles':
                for box in [self.line_box_para, self.line_box_norm]:
                    box.setSuffix('°')
                self.para_box_label.setText('Omega')
                self.norm_box_label.setText('2 Theta')
                signals_gui.get_angle_map.emit()

            case 'Reciprocal Vectors':
                for box in [self.line_box_para, self.line_box_norm]:
                    box.setSuffix(u' Å⁻¹')
                self.para_box_label.setText('q parallel')
                self.norm_box_label.setText('q normal')
                signals_gui.get_q_map.emit()