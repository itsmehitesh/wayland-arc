import time
import random
from src.data import TelemetryDatabase
from src.vision import WeldVisionSystem
from src.motion import MotionGantry

SIMULATE_CELL = True
TARGET_AXIS_TRAVEL = 100
FEEDRATE_MM_S = 5

def start_production_run():
    print("[WAYLAND SYSTEM] Initializing cell architecture modules...")
    
    db = TelemetryDatabase()
    vision = WeldVisionSystem(simulate=SIMULATE_CELL)
    gantry = MotionGantry(simulate=SIMULATE_CELL)
    
    print("[WAYLAND SYSTEM] Safe operations validation clear. Beginning cycle loop.")
    position_step = 0.0
    
    try:
        while position_step < TARGET_AXIS_TRAVEL:
            # Command Linear Step
            gantry.move_x(position_step)
            
            # Fetch Telemetry Frames and Metrics
            _, width_measurement = vision.process_frame()
            
            # Generate simulated power electronics inputs
            volts = 24.0 + random.uniform(-0.4, 0.4)
            amps = 150.0 + random.uniform(-1.5, 1.5)
            
            # Write to Time-Series Engine
            db.log_reading(position_step, width_measurement, volts, amps)
            print(f"[CYCLE] X: {position_step:.1f}mm | Width: {width_measurement:.2f}mm | V: {volts:.1f}V | A: {amps:.0f}A")
            
            position_step += (FEEDRATE_MM_S * 0.1)
            time.sleep(0.1)
            
        print("[WAYLAND SYSTEM] Production routine completed normally.")

    except KeyboardInterrupt:
        # Catch normal terminal breaks and fire standard E-Stop execution
        gantry.emergency_stop()
    finally:
        vision.cleanup()
        gantry.cleanup()

if __name__ == "__main__":
    while True:
        start_production_run()
        time.sleep(3)