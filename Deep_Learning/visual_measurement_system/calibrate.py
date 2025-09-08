# calibrate.py
import cv2
import numpy as np

class Calibrator:
    def __init__(self):
        self.mm_per_px = None

    def calibrate_from_line(self, img, p1, p2, real_mm):
        """
        p1, p2: iki pixel koordinatı (x,y) formatında
        real_mm: bu iki nokta arası gerçek uzunluk (mm)
        """
        px_dist = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** 0.5
        if px_dist == 0:
            raise ValueError("Pixel mesafesi 0, hatalı noktalar.")
        self.mm_per_px = real_mm / px_dist
        return self.mm_per_px

    def calibrate_with_marker(self, img, marker_contour, real_mm):
        # marker_contour: konturun bounding box uzunluğu piksellerde
        x,y,w,h = cv2.boundingRect(marker_contour)
        px_len = max(w,h)
        self.mm_per_px = real_mm / px_len
        return self.mm_per_px

    def px2mm(self, px):
        if self.mm_per_px is None:
            raise RuntimeError("Kalibrasyon yapılmadı.")
        return px * self.mm_per_px
