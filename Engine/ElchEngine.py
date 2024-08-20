import numpy as np
import xrayutilities as xu

from Signals.Signals import signals_engine, signals_gui


class ElchEngine:
    def __init__(self):
        self.raw_file = None

        self.res = None

        self.om = None
        self.tt = None
        self.counts = None

        self.q_norm = None
        self.q_para = None
        self.q_counts = None

        signals_gui.load_file.connect(self.load_file)
        signals_gui.get_angle_map.connect(lambda: signals_engine.map_data_angle.emit(self.get_angle_data()))
        signals_gui.get_q_map.connect(lambda: signals_engine.map_data_q.emit(self.get_q_data()))
        signals_gui.get_line_scan.connect(self.get_line_scan)

    def load_file(self, path):
        raw_file = xu.io.XRDMLFile(path)
        self.tt = raw_file.scan.ddict['2Theta']
        self.om = raw_file.scan.ddict['Omega']
        self.om = np.broadcast_to(self.om.reshape(-1, 1), self.tt.shape)
        self.counts = raw_file.scan.ddict['counts']

        self.ang_to_q()

        signals_engine.map_data_angle.emit(self.get_angle_data())

    def ang_to_q(self):
        k = 1.5405980
        om = self.om * np.pi / 180
        tt = self.tt * np.pi / 180
        q_norm = 1 / k * (np.sin(tt - om) + np.sin(om))
        q_para = 1 / k * (np.cos(tt - om) - np.cos(om))

        self.res = np.min(tt.shape)
        gd = xu.Gridder2D(self.res, self.res)
        gd(q_para, q_norm, self.counts)

        self.q_para = gd.xmatrix
        self.q_norm = gd.ymatrix
        self.q_counts = gd.data

    def get_angle_data(self):
        return {'om': self.om, 'tt': self.tt, 'counts': self.counts}

    def get_q_data(self):
        return {'q_para': self.q_para, 'q_norm': self.q_norm, 'q_counts': self.q_counts}

    def get_line_scan(self, pos_1, pos_2, scan_type, coord_type):
        match coord_type:
            case 'Reciprocal Vectors':
                qy = pos_1
                qz = pos_2
            case 'Angles':
                k = 1.5405980
                qy = 1 / k * (np.cos(pos_2 / 180 * np.pi - pos_1 / 180 * np.pi) - np.cos(pos_1 / 180 * np.pi))
                qz = 1 / k * (np.sin(pos_2 / 180 * np.pi - pos_1 / 180 * np.pi) + np.sin(pos_1 / 180 * np.pi))

        match scan_type:
            case 'Q Parallel':
                x, y, _ = xu.analysis.line_cuts.get_qy_scan([self.q_para, self.q_norm], self.q_counts, qz, self.res,
                                                            0.01)
                signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'q_parallel'})
            case 'Q Normal':
                x, y, _ = xu.analysis.line_cuts.get_qz_scan([self.q_para, self.q_norm], self.q_counts, qy, self.res,
                                                            0.01)
                signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'q_normal'})
            case 'Omega':
                x, y, _ = xu.analysis.line_cuts.get_omega_scan([self.q_para, self.q_norm], self.q_counts, [qy, qz],
                                                               self.res, 0.01)
                signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'omega'})
            case '2 Theta':
                x, y, _ = xu.analysis.line_cuts.get_ttheta_scan([self.q_para, self.q_norm], self.q_counts, [qy, qz],
                                                                self.res, 0.01)
                signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': '2theta'})
            case 'Radial':
                x, y, _ = xu.analysis.line_cuts.get_radial_scan([self.q_para, self.q_norm], self.q_counts, [qy, qz],
                                                                self.res, 0.01)
                signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'radial'})
