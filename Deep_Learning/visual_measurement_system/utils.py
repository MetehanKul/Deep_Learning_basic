import cv2
import numpy as np
import os

def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return cv2.imread(path)

def measure_dimensions(img, calibration_mm=10, calibration_px=50):
    """
    Görseldeki parçanın tam boy, genişlik ve çapını hesaplar.
    """
    px_to_mm = calibration_mm / calibration_px
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    contour = max(contours, key=cv2.contourArea)

    # Bounding box → tam boy ve genişlik
    x, y, w, h = cv2.boundingRect(contour)
    tam_boy_mm = h * px_to_mm
    genislik_mm = w * px_to_mm

    # En küçük daire → çap
    (xc, yc), radius = cv2.minEnclosingCircle(contour)
    cap_mm = (2 * radius) * px_to_mm

    results = {
        "tam_boy_mm": tam_boy_mm,
        "genislik_mm": genislik_mm,
        "cap_mm": cap_mm,
        "bbox": (x, y, w, h),
        "circle": (int(xc), int(yc), int(radius))
    }

    return results

def draw_measurements(img, results):
    if results is None:
        return img

    x, y, w, h = results["bbox"]
    xc, yc, radius = results["circle"]

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(img, (xc, yc), radius, (255, 0, 0), 2)

    cv2.putText(img, f"Boy: {results['tam_boy_mm']:.2f} mm", (x, y - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"Genişlik: {results['genislik_mm']:.2f} mm", (x, y - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"Cap: {results['cap_mm']:.2f} mm", (xc, yc),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    return img
