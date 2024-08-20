from PySide6.QtCore import QObject, Signal


class GuiSignals(QObject):
    load_file = Signal(str)
    get_angle_map = Signal()
    get_q_map = Signal()


class EngineSignals(QObject):
    map_data_angle = Signal(dict)
    map_data_q = Signal(dict)


signals_engine = EngineSignals()
signals_gui = GuiSignals()
