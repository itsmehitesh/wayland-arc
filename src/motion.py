import serial
import time

class MotionGantry:
    """Controls the 2-axis torch/camera positioning gantry"""
    def __init__(self, port='/dev/tty.usbserial', baudrate=115200, simulate=True):
        self.simulate = simulate
        self.current_x = 0.0
        self.serial_conn = None
        self.estop_active = False
        
        if not self.simulate:
            try:
                self.serial_conn = serial.Serial(port, baudrate, timeout=1)
                time.sleep(2) 
                self.send_command("$X") 
            except Exception as e:
                print(f"[MOTION] Hardware connect failed, defaulting to simulation: {e}")
                self.simulate = True

    def send_command(self, cmd):
        if self.estop_active:
            print("[MOTION] REJECTED: E-Stop is active!")
            return "ERROR: ESTOP"
        if self.simulate:
            return "ok"
        self.serial_conn.write((cmd + '\n').encode())
        return self.serial_conn.readline().decode().strip()

    def move_x(self, target_x, feedrate=500):
        if self.estop_active:
            return
        self.current_x = target_x
        cmd = f"G01 X{target_x} F{feedrate}"
        self.send_command(cmd)

    def emergency_stop(self):
        """Triggers an immediate software/hardware override to halt all execution"""
        self.estop_active = True
        print("\n🚨 [E-STOP] CRITICAL: INTERRUPT SIGNAL RECEIVED. HALTING ALL AXES.")
        if not self.simulate and self.serial_conn:
            self.serial_conn.write(b'!') 
            self.serial_conn.flush()

    def cleanup(self):
        if self.serial_conn:
            self.serial_conn.close()