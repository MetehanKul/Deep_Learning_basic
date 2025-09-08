# measurement.py
import cv2
import numpy as np
from calibrate import Calibrator

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    return blur

def find_contours(img):
    blur = preprocess(img)
    edged = cv2.Canny(blur, 50, 150)
    cnts, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cnts, edged

def largest_contour(cnts):
    if not cnts:
        return None
    return max(cnts, key=cv2.contourArea)

def measure_distance_between_points(p1, p2, calibrator: Calibrator):
    px = np.linalg.norm(np.array(p1) - np.array(p2))
    return calibrator.px2mm(px)

def measure_bounding_box_dim(contour, calibrator: Calibrator):
    x,y,w,h = cv2.boundingRect(contour)
    return calibrator.px2mm(w), calibrator.px2mm(h)  # width_mm, height_mm

def measure_circle(contour, calibrator: Calibrator):
    # fit minimum enclosing circle
    (x,y), radius = cv2.minEnclosingCircle(contour)
    diameter_px = 2 * radius
    return calibrator.px2mm(diameter_px)

def draw_result(img, text, ok=True, pos=(30,30)):
    color = (0,255,0) if ok else (0,0,255)
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    # draw a circle (status)
    cv2.circle(img, (pos[0]-25,pos[1]-5), 10, color, -1)
