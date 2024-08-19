from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QVBoxLayout, QPushButton


class ElchFileMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons = {key: QPushButton(parent=self, text=key, objectName=key)
                        for key in ['Open File', 'Export Data', 'Save Plots']}
        self.select_buttons = {key: QCheckBox(parent=self, text=key, objectName=key)
                               for key in ['Angle Map', 'Reciprocal Space Map', 'Omega Scan', '2 Theta Scan',
                                           'Q Parallel scan', 'Q Normal Scan']}

        vbox = QVBoxLayout()
        vbox.setSpacing(10)
        vbox.setContentsMargins(10, 10, 10, 10)

        vbox.addWidget(QLabel(text='File input', objectName='Header'), stretch=0)
        vbox.addWidget(self.buttons['Open File'], stretch=0)

        vbox.addSpacing(20)

        vbox.addWidget(QLabel(text='File export', objectName='Header'))
        for key, button in self.select_buttons.items():
            vbox.addWidget(button)
        vbox.addSpacing(10)
        vbox.addWidget(self.buttons['Export Data'])
        vbox.addWidget(self.buttons['Save Plots'])

        vbox.addStretch()
        self.setLayout(vbox)
