class SafetyAlertSystem:
    """Monitors live tolerances and triggers control alerts for operators"""
    def __init__(self, cpk_target=1.33):
        self.cpk_target = cpk_target
        self.errors = []

    def check_tolerances(self, current_width, usl, lsl, current_cpk):
        self.errors.clear()
        if current_width > usl:
            self.errors.append(f"OUT OF SPEC: Measured width ({current_width:.2f}mm) exceeds upper limit ({usl}mm)")
        elif current_width < lsl:
            self.errors.append(f"OUT OF SPEC: Measured width ({current_width:.2f}mm) drops below lower limit ({lsl}mm)")
        if 0 < current_cpk < self.cpk_target:
            self.errors.append(f"STABILITY WARNING: Process Cpk ({current_cpk:.2f}) is below target threshold ({self.cpk_target})")
        return self.errors