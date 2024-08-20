from PySide6.QtCore import QObject, Signal


class GuiSignals(QObject):
    load_file = Signal(str)


class EngineSignals(QObject):
    map_data_angle = Signal(dict)
    map_data_reciprocal = Signal(dict)


signals_engine = EngineSignals()
signals_gui = GuiSignals()
