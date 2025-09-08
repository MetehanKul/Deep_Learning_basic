# camera_thread.py
import cv2
import threading
import time

class CameraThread(threading.Thread):
    def __init__(self, src=0, fps=30):
        super().__init__()
        self.src = src
        self.fps = fps
        self.cap = cv2.VideoCapture(self.src)
        self.running = False
        self.frame = None

    def run(self):
        self.running = True
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue
            self.frame = frame
            time.sleep(1/self.fps)

    def stop(self):
        self.running = False
        time.sleep(0.1)
        if self.cap:
            self.cap.release()

    def get_frame(self):
        return self.frame
