import cv2
import numpy as np

PIXEL_TO_MM = 0.0264583  # Kalibrasyonunuza göre ayarlayın

def otomatik_cap_olc(img, pixel_to_mm=1.0, min_area=1000):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 100, 200)
    kernel = np.ones((5, 5), np.uint8)
    img_dilated = cv2.dilate(img_canny, kernel, iterations=2)
    img_eroded = cv2.erode(img_dilated, kernel, iterations=1)

    contours, _ = cv2.findContours(img_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    renkler = [
        (0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 255),
        (255, 0, 255), (255, 255, 0), (128, 0, 128), (0, 128, 255),
        (128, 255, 0), (255, 128, 0),
    ]
    for idx, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > min_area:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            diameter_px = 2 * radius
            diameter_mm = diameter_px * pixel_to_mm
            renk = renkler[idx % len(renkler)]
            cv2.circle(img, center, radius, renk, 2)
            cv2.putText(
                img,
                f"Cap: {diameter_px}px ({diameter_mm:.2f}mm)",
                (center[0] - 40, center[1] - radius - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                renk,
                2
            )
    return img

# Fotoğraf yolu
image_path = "dataset/test/OK/3.jpg"  # Buraya kendi fotoğraf dosya adınızı yazın

img = cv2.imread(image_path)
if img is None:
    print("Resim bulunamadı!")
else:
    display = otomatik_cap_olc(img, pixel_to_mm=PIXEL_TO_MM, min_area=1000)
    cv2.imshow("Otomatik Cap Olcumu", display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()