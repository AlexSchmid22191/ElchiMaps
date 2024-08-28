import functools as ft
import os.path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QPushButton, QFileDialog, QLabel, QGridLayout

from Signals.Signals import signals_gui


class ElchExport(QDialog):
    def __init__(self, options, last_path, file_fmt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.options = options
        self.last_path = last_path
        self.file_fmt = file_fmt
        self.setWindowTitle("Export Data")

        self.option_labels = {option: QLabel(text=option) for option in options}
        self.browse_buttons = {option: QPushButton("Save as") for option in options}

        grid_layout = QGridLayout()
        for idx, option in enumerate(options):
            grid_layout.addWidget(self.option_labels[option], idx, 0)
            grid_layout.addWidget(self.browse_buttons[option], idx, 2)
            self.browse_buttons[option].setMinimumWidth(150)

            self.browse_buttons[option].clicked.connect(
                ft.partial(self.browse_file, option))

        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close)
        grid_layout.addWidget(self.close_button, 3, 0, 1, 3)

        self.setLayout(grid_layout)

    def browse_file(self, option_name):
        file_dialog = QFileDialog(self, self.last_path)
        file_dialog.setWindowTitle(f"Export path for {option_name}")
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_path, _ = file_dialog.getSaveFileName(self, f"Select Path for {option_name}")

        if file_path:
            if os.path.splitext(file_path)[1] != self.file_fmt:
                file_path += self.file_fmt
        self.last_path = file_path
        signals_gui.export_data.emit({'option': option_name, 'file_path': file_path})
