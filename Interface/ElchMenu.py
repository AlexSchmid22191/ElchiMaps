import os

import matplotlib.pyplot as plt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QRadioButton, QButtonGroup, QVBoxLayout, QLabel, QDoubleSpinBox, \
    QHBoxLayout, QComboBox, QFileDialog

from Interface.ElchExport import ElchExport
from Signals.Signals import signals_gui, signals_engine


class ElchMenu(QWidget):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setFixedWidth(260)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.file_button = QPushButton(parent=self, text='Open File', objectName='Open File')

        self.plot_buttons = {key: QPushButton(parent=self, text=key, objectName=key) for key in ['Autoscale', 'Zoom']}
        self.plot_buttons['Zoom'].setCheckable(True)

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

        self.para_box_label = QLabel(text='Omega')
        self.norm_box_label = QLabel(text='2 Theta')
        self.line_box_para = QDoubleSpinBox(decimals=4, singleStep=1e-2, minimum=-180, maximum=180, suffix=u'°',
                                            value=30)
        self.line_box_norm = QDoubleSpinBox(decimals=4, singleStep=1e-2, minimum=-180, maximum=180, suffix=u'°',
                                            value=60)

        self.color_select = QComboBox()
        self.color_select.addItems(plt.colormaps())

        self.int_dir_select = QComboBox()
        self.int_dir_select.addItems(['2 Theta', 'Radial'])
        self.int_dist_select = QDoubleSpinBox(decimals=3, singleStep=1e-3, minimum=0, value=0.01)

        self.export_button = QPushButton(parent=self, text='Export')

        self.file_open_path = os.path.expanduser('~')
        self.file_export_path = os.path.expanduser('~')

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(text='File IO', objectName='Header'))
        vbox.addWidget(self.file_button)
        vbox.addWidget(self.export_button)
        vbox.addSpacing(20)

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

        vbox.addWidget(QLabel(text='Plotting Control', objectName='Header'))
        for button in self.plot_buttons.values():
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
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(text='Integration distance'))
        hbox.addWidget(self.int_dist_select)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(text='Integration direction'))
        hbox.addWidget(self.int_dir_select)
        vbox.addLayout(hbox)


        vbox.addStretch()
        vbox.setSpacing(10)
        vbox.setContentsMargins(10, 10, 10, 10)
        self.setLayout(vbox)

        self.coordinate_check_group.buttonClicked.connect(self.change_coordinates)
        self.line_box_para.valueChanged.connect(self.request_line_scan)
        self.line_box_norm.valueChanged.connect(self.request_line_scan)
        self.line_check_group.buttonClicked.connect(self.on_scan_select)
        self.int_dist_select.valueChanged.connect(self.request_line_scan)
        self.int_dir_select.currentTextChanged.connect(self.on_int_dir_select)
        self.file_button.clicked.connect(self.open_file)

        self.export_button.clicked.connect(self.export)

        self.coordinate_checks['Angles'].setChecked(True)
        self.line_checks['Omega'].setChecked(True)
        signals_gui.load_file.connect(lambda: self.coordinate_checks['Angles'].setChecked(True))
        signals_engine.q_to_ang.connect(self.update_line_cut_boxes)
        signals_engine.ang_to_q.connect(self.update_line_cut_boxes)

    def change_coordinates(self, button):
        match button.objectName():
            case 'Angles':
                for box in [self.line_box_para, self.line_box_norm]:
                    box.setSuffix('°')
                    box.setSingleStep(1e-2)
                self.para_box_label.setText('Omega')
                self.norm_box_label.setText('2 Theta')
                signals_gui.q_to_ang.emit(self.line_box_para.value(), self.line_box_norm.value())
                signals_gui.get_angle_map.emit()

            case 'Reciprocal Vectors':
                for box in [self.line_box_para, self.line_box_norm]:
                    box.setSuffix(u' Å⁻¹')
                    box.setSingleStep(1e-3)
                self.para_box_label.setText('q parallel')
                self.norm_box_label.setText('q normal')
                signals_gui.ang_to_q.emit(self.line_box_para.value(), self.line_box_norm.value())
                signals_gui.get_q_map.emit()

    def request_line_scan(self):
        signals_gui.get_line_scan.emit(self.line_box_para.value(), self.line_box_norm.value(),
                                       self.int_dist_select.value(), self.line_check_group.checkedButton().objectName(),
                                       self.coordinate_check_group.checkedButton().objectName(),
                                       self.int_dir_select.currentText())

    def on_scan_select(self):
        self.update_int_dir()
        self.update_int_dist()
        self.request_line_scan()

    def on_int_dir_select(self):
        self.update_int_dist()
        self.request_line_scan()

    def update_int_dir(self):
        self.int_dir_select.blockSignals(True)
        self.int_dir_select.clear()
        match self.line_check_group.checkedButton().objectName():
            case 'Omega':
                self.int_dir_select.addItems(['2 Theta', 'Radial'])
            case '2 Theta':
                self.int_dir_select.addItems(['Omega', 'Radial'])
            case 'Radial':
                self.int_dir_select.addItems(['2 Theta', 'Omega'])
            case 'Q Normal':
                self.int_dir_select.addItems(['Q Parallel', '2 Theta', 'Omega'])
            case 'Q Parallel':
                self.int_dir_select.addItems(['Q Normal', '2 Theta', 'Omega'])
        self.int_dir_select.blockSignals(False)

    def update_int_dist(self):
        int_dir = self.int_dir_select.currentText()
        self.int_dist_select.blockSignals(True)
        match int_dir:
            case 'Omega' | '2 Theta' | 'Radial':
                self.int_dist_select.setSuffix('°')
            case 'Q Parallel' | 'Q Normal':
                self.int_dist_select.setSuffix(u' Å⁻¹')
        self.int_dist_select.blockSignals(False)

    def update_line_cut_boxes(self, pos_para, pos_norm):
        for box in [self.line_box_para, self.line_box_norm]:
            box.blockSignals(True)
        self.line_box_para.setValue(pos_para)
        self.line_box_norm.setValue(pos_norm)
        for box in [self.line_box_para, self.line_box_norm]:
            box.blockSignals(False)

    def open_file(self):
        filepath, *_ = QFileDialog.getOpenFileName(self, 'Select XRDML file', self.file_open_path,
                                                   'XRDML files (*.xrdml)')
        self.file_open_path = os.path.dirname(filepath)
        if filepath.endswith('.xrdml'):
            signals_gui.load_file.emit(filepath)

    def export(self):
        dialog = ElchExport(last_path=self.file_export_path, parent=self)
        if dialog.exec():
            self.file_export_path = os.path.dirname(dialog.last_path)
