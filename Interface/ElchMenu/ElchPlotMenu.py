import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QLabel, QDoubleSpinBox, \
    QHBoxLayout, QComboBox

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

        self.normalize_buttons = {key: QRadioButton(parent=self, text=key, objectName=key)
                                  for key in ['Linear', 'Logarithmic', 'Square Root']}
        self.normalize_group = QButtonGroup()
        self.normalize_group.setExclusive(True)
        self.normalize_buttons['Linear'].setChecked(True)

        self.line_checks = {key: QRadioButton(parent=self, text=key, objectName=key)
                            for key in ['Omega', '2 Theta', 'Radial', 'Q Parallel', 'Q Normal']}
        self.line_check_group = QButtonGroup()
        self.line_check_group.setExclusive(True)
        self.line_checks['Omega'].setChecked(True)

        self.para_box_label = QLabel(text='Omega')
        self.norm_box_label = QLabel(text='2 Theta')
        self.line_box_para = QDoubleSpinBox(decimals=4, singleStep=1e-2, minimum=0, maximum=180, suffix=u'°', value=45)
        self.line_box_norm = QDoubleSpinBox(decimals=4, singleStep=1e-2, minimum=0, maximum=180, suffix=u'°', value=90)

        self.color_select = QComboBox()
        self.color_select.addItems(plt.colormaps())

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(text='Coordinate System', objectName='Header'))
        for key, button in self.coordinate_checks.items():
            self.coordinate_check_group.addButton(button)
            vbox.addWidget(button)
        vbox.addSpacing(20)

        vbox.addWidget(QLabel(text='Normalization', objectName='Header'))
        for key, button in self.normalize_buttons.items():
            self.normalize_group.addButton(button)
            vbox.addWidget(button)
        vbox.addSpacing(20)

        vbox.addWidget(QLabel(text='Colormap', objectName='Header'))
        vbox.addWidget(self.color_select)
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
        self.line_box_para.valueChanged.connect(self.request_line_scan)
        self.line_box_norm.valueChanged.connect(self.request_line_scan)
        self.line_check_group.buttonClicked.connect(self.request_line_scan)

        self.coordinate_checks['Angles'].setChecked(True)
        signals_gui.load_file.connect(lambda: self.coordinate_checks['Angles'].setChecked(True))

    def change_coordinates(self, button):
        match button.objectName():
            case 'Angles':
                for box in [self.line_box_para, self.line_box_norm]:
                    box.setSuffix('°')
                self.para_box_label.setText('Omega')
                self.norm_box_label.setText('2 Theta')

                qy = self.line_box_para.value()
                qz = self.line_box_norm.value()
                k = 1.5405980
                q = np.sqrt(qy**2 + qz**2)
                tt = 2 * np.arcsin(q*k/2) * 180 / np.pi
                om = np.arccos(qy*k) * 180 / np.pi - 90 + tt/2

                self.line_box_para.setValue(om)
                self.line_box_norm.setValue(tt)
                signals_gui.get_angle_map.emit()

            case 'Reciprocal Vectors':
                for box in [self.line_box_para, self.line_box_norm]:
                    box.setSuffix(u' Å⁻¹')
                self.para_box_label.setText('q parallel')
                self.norm_box_label.setText('q normal')

                om = self.line_box_para.value()
                tt = self.line_box_norm.value()
                k = 1.5405980
                qy = 1 / k * (np.cos(tt / 180 * np.pi - om / 180 * np.pi) - np.cos(om / 180 * np.pi))
                qz = 1 / k * (np.sin(tt / 180 * np.pi - om / 180 * np.pi) + np.sin(om / 180 * np.pi))
                self.line_box_para.setValue(qy)
                self.line_box_norm.setValue(qz)
                signals_gui.get_q_map.emit()

    def request_line_scan(self):
        signals_gui.get_line_scan.emit(self.line_box_para.value(), self.line_box_norm.value(),
                                       self.line_check_group.checkedButton().objectName(),
                                       self.coordinate_check_group.checkedButton().objectName())


# TODO: Convert the values in the line cut position entries when switching coordinate systems