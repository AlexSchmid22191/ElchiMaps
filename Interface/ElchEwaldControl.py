from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider, QCheckBox, QLabel, QGridLayout
from PySide6.QtWidgets import QWidget

from Signals.Signals import signals_gui, signals_engine


class ElchEwaldControl(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.om_slider = QSlider(orientation=Qt.Orientation(Qt.Horizontal))
        self.tt_slider = QSlider(orientation=Qt.Orientation(Qt.Horizontal))
        self.wl_slider = QSlider(orientation=Qt.Orientation(Qt.Horizontal))
        self.om_label = QLabel(text='30°')
        self.tt_label = QLabel(text='60°')
        self.wl_label = QLabel(text='1.54 Å')
        self.q_para_label = QLabel('0.000  Å⁻¹')
        self.q_norm_label = QLabel('0.000  Å⁻¹')
        self.rad_check_box = QCheckBox()

        self.om_slider.setMinimum(0)
        self.om_slider.setMaximum(180)
        self.tt_slider.setMinimum(0)
        self.tt_slider.setMaximum(180)
        self.wl_slider.setMinimum(100)
        self.wl_slider.setMaximum(200)

        self.om_slider.setValue(30)
        self.tt_slider.setValue(60)
        self.wl_slider.setValue(154)

        self.const_ang = self.om_slider.value() + 90 - self.tt_slider.value() / 2

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        grid_layout.addWidget(QLabel(text='Omega'), 0, 0)
        grid_layout.addWidget(QLabel(text='2 Theta'), 1, 0)
        grid_layout.addWidget(QLabel(text='Wavelength'), 2, 0)
        grid_layout.addWidget(self.om_slider, 0, 1)
        grid_layout.addWidget(self.tt_slider, 1, 1)
        grid_layout.addWidget(self.wl_slider, 2, 1)
        grid_layout.addWidget(self.om_label, 0, 2)
        grid_layout.addWidget(self.tt_label, 1, 2)
        grid_layout.addWidget(self.wl_label, 2, 2)
        grid_layout.setColumnMinimumWidth(3, 30)
        grid_layout.addWidget(QLabel('Q Parallel:'), 0, 4)
        grid_layout.addWidget(QLabel('Q Normal:'), 1, 4)
        grid_layout.addWidget(QLabel('Radial scan'), 2, 4)
        grid_layout.addWidget(self.q_para_label, 0, 5)
        grid_layout.addWidget(self.q_norm_label, 1, 5)
        grid_layout.addWidget(self.rad_check_box, 2, 5)

        self.setLayout(grid_layout)

        self.om_slider.valueChanged.connect(self.on_omega_slider)
        self.tt_slider.valueChanged.connect(self.on_tt_slider)
        self.wl_slider.valueChanged.connect(self.on_wl_slider)
        signals_engine.ang_to_q.connect(self.update_q_labels)

    def on_omega_slider(self, *args):
        self.om_label.setText(f'{self.om_slider.value():}°')

        if self.rad_check_box.isChecked():
            self.tt_slider.setValue(2 * (self.om_slider.value() + 90 - self.const_ang))
        else:
            self.const_ang = self.om_slider.value() + 90 - self.tt_slider.value() / 2

        signals_gui.ang_to_q.emit(self.om_slider.value(), self.tt_slider.value())
        signals_gui.get_ewald.emit(self.om_slider.value(), self.tt_slider.value(), self.wl_slider.value() / 100)

    def on_tt_slider(self, *args):
        self.tt_label.setText(f'{self.tt_slider.value()}°')

        if self.rad_check_box.isChecked():
            self.om_slider.setValue(self.const_ang + self.tt_slider.value() / 2 - 90)
        else:
            self.const_ang = self.om_slider.value() + 90 - self.tt_slider.value() / 2

        signals_gui.ang_to_q.emit(self.om_slider.value(), self.tt_slider.value())
        signals_gui.get_ewald.emit(self.om_slider.value(), self.tt_slider.value(), self.wl_slider.value() / 100)

    def update_q_labels(self, q_para, q_norm):
        self.q_para_label.setText(f'{q_para:.3f} Å⁻¹')
        self.q_norm_label.setText(f'{q_norm:.3f} Å⁻¹')

    def on_wl_slider(self):
        self.wl_label.setText(f'{self.wl_slider.value() / 100:.2f} Å')
        signals_gui.get_ewald.emit(self.om_slider.value(), self.tt_slider.value(), self.wl_slider.value() / 100)
