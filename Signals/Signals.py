from PySide6.QtCore import QObject, Signal


class GuiSignals(QObject):
    load_file = Signal(str)
    get_angle_map = Signal()
    get_q_map = Signal()
    get_line_scan = Signal(float, float, float, str, str, str)
    ang_to_q = Signal(float, float)
    q_to_ang = Signal(float, float)
    get_ewald = Signal(float, float, float)
    export_data = Signal(dict)
    export_images = Signal(dict)


class EngineSignals(QObject):
    map_data_angle = Signal(dict)
    map_data_q = Signal(dict)
    line_scan_1D = Signal(dict)
    line_Scan_2D = Signal(dict)
    ang_to_q = Signal(float, float)
    q_to_ang = Signal(float, float)
    ewald = Signal(dict)


signals_engine = EngineSignals()
signals_gui = GuiSignals()
