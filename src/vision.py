import cv2
import numpy as np
import random
import time

class WeldVisionSystem:
    """Computer vision pipeline for geometry tracking and feature extraction"""
    def __init__(self, simulate=True, source=0):
        self.simulate = simulate
        self.source = source
        self.cap = None
        if not self.simulate:
            self.cap = cv2.VideoCapture(self.source)

    def process_frame(self):
        if self.simulate:
            time.sleep(0.1) 
            simulated_width = 10.0 + np.sin(time.time()) + random.uniform(-0.5, 0.5)
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, f"VISION SIMULATION ACTIVE: {simulated_width:.2f}mm", 
                        (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            return frame, simulated_width

        ret, frame = self.cap.read()
        if not ret:
            return None, 0.0
        return frame, 10.0 # Placeholder value for webcam check

    def cleanup(self):
        if self.cap:
            self.cap.release()