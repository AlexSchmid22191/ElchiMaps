import numpy as np
import xrayutilities as xu

from Signals.Signals import signals_engine, signals_gui


class ElchEngine:
    def __init__(self):
        self.raw_file = None

        self.om = None
        self.tt = None
        self.counts = None

        self.q_norm = None
        self.q_para = None
        self.q_counts = None

        signals_gui.load_file.connect(self.load_file)

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

        res = np.min(tt.shape)
        gd = xu.Gridder2D(res, res)
        gd(q_para, q_norm, self.counts)

        self.q_para = gd.xmatrix
        self.q_norm = gd.ymatrix
        self.q_counts = gd.data

    def get_angle_data(self):
        return {'om': self.om, 'tt': self.tt, 'counts': self.counts}

    def get_q_data(self):
        return {'q_para': self.q_para, 'q_norm': self.q_norm, 'q_counts': self.q_counts}
