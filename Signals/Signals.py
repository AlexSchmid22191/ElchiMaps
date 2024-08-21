from PySide6.QtCore import QObject, Signal


class GuiSignals(QObject):
    load_file = Signal(str)
    get_angle_map = Signal()
    get_q_map = Signal()
    get_line_scan = Signal(float, float, str, str)
    ang_to_q = Signal(float, float)
    q_to_ang = Signal(float, float)


class EngineSignals(QObject):
    map_data_angle = Signal(dict)
    map_data_q = Signal(dict)
    line_scan_1D = Signal(dict)
    line_Scan_2D = Signal(dict)
    ang_to_q = Signal(float, float)
    q_to_ang = Signal(float, float)


signals_engine = EngineSignals()
signals_gui = GuiSignals()
