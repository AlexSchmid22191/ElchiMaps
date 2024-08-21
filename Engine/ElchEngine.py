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

        self.wl = 1.5405980
        self.k = 2 * np.pi / self.wl

        self.qy_range = None
        self.qz_range = None
        self.om_range = None
        self.tt_range = None

        signals_gui.load_file.connect(self.load_file)
        signals_gui.get_angle_map.connect(lambda: signals_engine.map_data_angle.emit(self.get_angle_data()))
        signals_gui.get_q_map.connect(lambda: signals_engine.map_data_q.emit(self.get_q_data()))
        signals_gui.get_angle_map.connect(lambda: signals_engine.line_Scan_2D.emit({'x': self.om_range, 'y': self.tt_range}))
        signals_gui.get_q_map.connect(lambda: signals_engine.line_Scan_2D.emit({'x': self.qy_range, 'y': self.qz_range}))

        signals_gui.get_line_scan.connect(self.get_line_scan)
        signals_gui.q_to_ang.connect(self.q_to_ang)
        signals_gui.ang_to_q.connect(self.ang_to_q)

    def load_file(self, path):
        self.raw_file = xu.io.XRDMLFile(path)
        self.tt = self.raw_file.scan.ddict['2Theta']
        self.om = self.raw_file.scan.ddict['Omega']
        self.om = np.broadcast_to(self.om.reshape(-1, 1), self.tt.shape)
        self.counts = self.raw_file.scan.ddict['counts']

        self.ang_map_to_q_map()

        signals_engine.map_data_angle.emit(self.get_angle_data())

    def ang_map_to_q_map(self):
        q_para, q_norm = self._atq(self.om, self.tt)
        self.res = np.min(self.tt.shape)
        gd = xu.Gridder2D(self.res, self.res)
        gd(q_para, q_norm, self.counts)

        self.q_para = gd.xmatrix
        self.q_norm = gd.ymatrix
        self.q_counts = gd.data

    def get_angle_data(self):
        return {'om': self.om, 'tt': self.tt, 'counts': self.counts}

    def get_q_data(self):
        return {'q_para': self.q_para, 'q_norm': self.q_norm, 'q_counts': self.q_counts}

    def _atq(self, om, tt):
        qy = self.k * (np.cos(tt / 180 * np.pi - om / 180 * np.pi) - np.cos(om / 180 * np.pi))
        qz = self.k * (np.sin(tt / 180 * np.pi - om / 180 * np.pi) + np.sin(om / 180 * np.pi))
        return qy, qz

    def _qta(self, qy, qz):
        q = np.sqrt(qy ** 2 + qz ** 2)
        tt = 2 * np.arcsin(q / self.k / 2) * 180 / np.pi
        om = np.arccos(qy / self.k) * 180 / np.pi - 90 + tt / 2
        return om, tt

    def ang_to_q(self, om, tt):
        qy, qz = self._atq(om, tt)
        signals_engine.ang_to_q.emit(qy, qz)

    def q_to_ang(self, qy, qz):
        om, tt = self._qta(qy, qz)
        signals_engine.q_to_ang.emit(om, tt)

    def get_line_scan(self, pos_1, pos_2, int_dist, scan_type, coord_type, int_dir):
        if self.raw_file is None:
            return
        match coord_type:
            case 'Reciprocal Vectors':
                qy = pos_1
                qz = pos_2
                om, tt = self._qta(qy, qz)
            case 'Angles':
                om = pos_1
                tt = pos_2
                qy, qz = self._atq(om, tt)

        match int_dir:
            case 'Omega':
                int_dir = 'omega'
            case '2 Theta':
                int_dir = '2theta'
            case 'Radial':
                int_dir = 'radial'
            case 'Q Parallel' | 'Q Normal':
                int_dir = 'q'

        match scan_type:
            case 'Q Parallel':
                try:
                    x, y, _ = xu.analysis.line_cuts.get_qy_scan([self.q_para, self.q_norm], self.q_counts, qz, self.res,
                                                                int_dist, intdir=int_dir)
                    self.qy_range = x
                    self.qz_range = np.full_like(self.qy_range, qz)
                    self.om_range, self.tt_range = self._qta(self.qy_range, self.qz_range)
                    signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'q_parallel'})
                except ValueError:
                    self.tt_range, self.om_range, self.qy_range, self.qz_range = None, None, None, None

            case 'Q Normal':
                try:
                    x, y, _ = xu.analysis.line_cuts.get_qz_scan([self.q_para, self.q_norm], self.q_counts, qy, self.res,
                                                            int_dist, intdir=int_dir)
                    self.qz_range = x
                    self.qy_range = np.full_like(self.qz_range, qy)
                    self.om_range, self.tt_range = self._qta(self.qy_range, self.qz_range)
                    signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'q_normal'})
                except ValueError:
                    self.tt_range, self.om_range, self.qy_range, self.qz_range = None, None, None, None

            case 'Omega':
                try:
                    x, y, _ = xu.analysis.line_cuts.get_omega_scan([self.q_para, self.q_norm], self.q_counts, [qy, qz],
                                                                   self.res, int_dist, intdir=int_dir)
                    self.om_range = x
                    self.tt_range = np.full_like(self.om_range, tt)
                    self.qz_range, self.qy_range = self._atq(self.om_range, self.tt_range)
                    signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'omega'})
                except ValueError:
                    self.tt_range, self.om_range, self.qy_range, self.qz_range = None, None, None, None

            case '2 Theta':
                try:
                    x, y, _ = xu.analysis.line_cuts.get_ttheta_scan([self.q_para, self.q_norm], self.q_counts, [qy, qz],
                                                                    self.res, int_dist, intdir=int_dir)
                    signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': '2theta'})
                    self.tt_range = x
                    self.om_range = np.full_like(self.tt_range, om)
                    self.qz_range, self.qy_range = self._atq(self.om_range, self.tt_range)
                except ValueError:
                    self.tt_range, self.om_range, self.qy_range, self.qz_range = None, None, None, None

            case 'Radial':
                try:
                    x, y, _ = xu.analysis.line_cuts.get_radial_scan([self.q_para, self.q_norm], self.q_counts, [qy, qz],
                                                                    self.res, int_dist, intdir=int_dir)
                    signals_engine.line_scan_1D.emit({'x': x, 'y': y, 'x_coord': 'radial'})

                    tau = 90 + tt/2 - om
                    self.tt_range = x
                    self.om_range = np.full_like(self.tt_range, 90 + self.tt_range - tau)
                    self.qz_range, self.qy_range = self._atq(self.om_range, self.tt_range)

                except ValueError:
                    self.tt_range, self.om_range, self.qy_range, self.qz_range = None, None, None, None

        match coord_type:
            case 'Reciprocal Vectors':
                signals_engine.line_Scan_2D.emit({'x': self.qy_range, 'y': self.qz_range})
            case 'Angles':
                signals_engine.line_Scan_2D.emit({'x': self.om_range, 'y': self.tt_range})
