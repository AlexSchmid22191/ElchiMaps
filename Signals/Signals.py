from PySide6.QtCore import QObject, Signal


class GuiSignals(QObject):
    load_file = Signal(str)
    get_angle_map = Signal()
    get_q_map = Signal()
    get_line_scan = Signal(float, float, str, str)


class EngineSignals(QObject):
    map_data_angle = Signal(dict)
    map_data_q = Signal(dict)
    line_scan_1D = Signal(dict)
    line_Scan_2D = Signal(dict)


signals_engine = EngineSignals()
signals_gui = GuiSignals()
