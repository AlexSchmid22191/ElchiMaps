from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from Interface.ElchMainWindow import ElchMainWindow


def main():
    app = QApplication()
    app.setWindowIcon(QIcon('Interface/Icons/Logo.ico'))
    gui = ElchMainWindow()
    app.exec()


if __name__ == '__main__':
    main()