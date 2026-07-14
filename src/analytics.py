import numpy as np

class StatisticalProcessControl:
    """Calculates process stability capability markers (Cp/Cpk, Control Limits)"""
    @staticmethod
    def calculate_cpk(data, usl, lsl):
        if len(data) < 2:
            return 0.0, 0.0
        mean = np.mean(data)
        std_dev = np.std(data, ddof=1)
        if std_dev == 0:
            return 0.0, 0.0
        cp = (usl - lsl) / (6 * std_dev)
        cpu = (usl - mean) / (3 * std_dev)
        cpl = (mean - lsl) / (3 * std_dev)
        return cp, min(cpu, cpl)

    @staticmethod
    def get_control_limits(data):
        if len(data) == 0:
            return 0, 0, 0
        mean = np.mean(data)
        std_dev = np.std(data, ddof=1)
        return mean, mean + (3 * std_dev), mean - (3 * std_dev)