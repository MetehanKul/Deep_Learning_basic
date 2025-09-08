# main.py
import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from db import init_db, save_part, save_measurement
from calibrate import Calibrator
from measurement import find_contours, largest_contour, measure_bounding_box_dim, measure_circle, draw_result
from camera_thread import CameraThread
from utils import load_image, measure_dimensions, draw_measurements

init_db()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Measurement System")
        self.setGeometry(100,100,1200,700)
        self.img = None
        self.display_img = None
        self.calibrator = Calibrator()
        self.camera_thread = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_camera_frame)

        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # top controls
        controls = QtWidgets.QHBoxLayout()
        self.load_btn = QtWidgets.QPushButton("Görsel Yükle")
        self.load_btn.clicked.connect(self.on_load_image)  # <-- değiştirildi
        controls.addWidget(self.load_btn)

        self.calib_btn = QtWidgets.QPushButton("Kalibrasyon (iki tıklama ile)")
        self.calib_btn.clicked.connect(self.start_calibration)
        controls.addWidget(self.calib_btn)

        self.start_cam_btn = QtWidgets.QPushButton("Kamerayı Başlat")
        self.start_cam_btn.clicked.connect(self.toggle_camera)
        controls.addWidget(self.start_cam_btn)

        layout.addLayout(controls)

        # image view
        self.label = QtWidgets.QLabel()
        self.label.setFixedSize(1000,600)
        self.label.setStyleSheet("background-color: #333;")
        layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

        # status
        self.status = QtWidgets.QLabel("Hazır")
        layout.addWidget(self.status)

        # mouse events for calibration / point selection
        self.label.mousePressEvent = self.on_mouse_press
        self.calib_points = []

    def update_image_label(self):
        if self.display_img is None:
            return
        h,w,ch = self.display_img.shape
        qimg = QtGui.QImage(self.display_img.data, w, h, 3*w, QtGui.QImage.Format_BGR888)
        pix = QtGui.QPixmap.fromImage(qimg).scaled(self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pix)

    def on_load_image(self):  # <-- fonksiyon adı değiştirildi
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Görsel Seç")
        print("Seçilen dosya:", path)  # <-- ekleyin
        if not path:
            return
        try:
            self.img = load_image(path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Görsel yüklenemedi:\n{e}")
            return
        self.display_img = self.img.copy()
        self.update_image_label()
        self.status.setText(f"Görsel yüklendi: {path.split('/')[-1]}")

    def start_calibration(self):
        self.status.setText("Kalibrasyon modu: görüntü üzerinde iki nokta tıklayın (bilinen mm girilecek).")
        self.calib_points = []

    def on_mouse_press(self, event):
        if self.img is None:
            return
        # map mouse pos to image pixel coordinates
        pix = self.label.pixmap()
        if not pix: return
        label_w, label_h = self.label.width(), self.label.height()
        pm_w, pm_h = pix.width(), pix.height()
        # compute offset
        x = event.pos().x() - (label_w - pm_w)//2
        y = event.pos().y() - (label_h - pm_h)//2
        if x < 0 or y < 0 or x > pm_w or y > pm_h:
            return
        # map to original image coords
        img_h, img_w = self.img.shape[:2]
        sx = x / pm_w
        sy = y / pm_h
        img_x = int(sx * img_w)
        img_y = int(sy * img_h)
        self.calib_points.append((img_x, img_y))
        # draw small circle
        cv2.circle(self.display_img, (img_x,img_y), 6, (255,0,0), -1)
        self.update_image_label()
        if len(self.calib_points) == 2:
            mm, ok = QtWidgets.QInputDialog.getDouble(self, "Gerçek uzunluk (mm)", "İki nokta arasındaki gerçek uzunluk (mm):", decimals=3)
            if ok:
                self.calibrator.calibrate_from_line(self.img, self.calib_points[0], self.calib_points[1], mm)
                self.status.setText(f"Kalibrasyon yapıldı: {self.calibrator.mm_per_px:.6f} mm/px")
            else:
                self.status.setText("Kalibrasyon iptal edildi.")
            self.calib_points = []

    def toggle_camera(self):
        if self.camera_thread and self.camera_thread.is_alive():
            self.camera_thread.stop()
            self.camera_thread = None
            self.timer.stop()
            self.start_cam_btn.setText("Kamerayı Başlat")
            self.status.setText("Kamera durdu.")
        else:
            self.camera_thread = CameraThread(src=0)
            self.camera_thread.start()
            self.timer.start(30)
            self.start_cam_btn.setText("Kamerayı Durdur")
            self.status.setText("Kamera çalışıyor...")

    def update_camera_frame(self):
        if not self.camera_thread:
            return
        frame = self.camera_thread.get_frame()
        if frame is None:
            return
        # quick measurement pipeline (example: find largest contour and measure bbox)
        display = frame.copy()
        cnts, edged = find_contours(frame)
        cnt = largest_contour(cnts) if cnts else None
        ok = False
        msg = "No part"
        if cnt is not None and self.calibrator.mm_per_px:
            w_mm, h_mm = measure_bounding_box_dim(cnt, self.calibrator)
            # For demo we assume we expect width=50mm tolerance 0.5mm (replace by DB value)
            ref_w = 50.0
            tol = 0.5
            ok = abs(w_mm - ref_w) <= tol
            msg = f"W: {w_mm:.2f} mm | H: {h_mm:.2f} mm | {'OK' if ok else 'NOK'}"
            # draw box
            x,y,w,h = cv2.boundingRect(cnt)
            color = (0,255,0) if ok else (0,0,255)
            cv2.rectangle(display, (x,y), (x+w, y+h), color, 2)
            draw_result(display, msg, ok=ok, pos=(30,50))
        else:
            cv2.putText(display, msg, (30,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200),2)

        # display
        self.display_img = display
        self.update_image_label()

teknik_resim_olculer = {
    "tam_boy_mm": 40.0,
    "genislik_mm": 24.0,
    "cap_mm": 20.0
}

tolerans = 1.0  # mm tolerans

def kontrol_et(measured, target, tol):
    return abs(measured - target) <= tol

if __name__ == "__main__":
    # Görseli yükle
    img = load_image("assets/2.jpg")

    # Ölçüm yap
    results = measure_dimensions(img, calibration_mm=10, calibration_px=50)

    if results is None:
        print("Parça algılanamadı.")
    else:
        print("Ölçülen değerler:", results)

        # Kontrol
        boy_ok = kontrol_et(results["tam_boy_mm"], teknik_resim_olculer["tam_boy_mm"], tolerans)
        genislik_ok = kontrol_et(results["genislik_mm"], teknik_resim_olculer["genislik_mm"], tolerans)
        cap_ok = kontrol_et(results["cap_mm"], teknik_resim_olculer["cap_mm"], tolerans)

        if boy_ok and genislik_ok and cap_ok:
            print("✅ Parça ölçüleri uygun (Yeşil Işık)")
            renk = (0, 255, 0)
        else:
            print("❌ Parça ölçüleri uygun değil (Kırmızı Işık)")
            renk = (0, 0, 255)

        # Görsel üzerine ölçüm çiz
        img = draw_measurements(img, results)
        cv2.putText(img, "OK" if renk == (0, 255, 0) else "NOT OK", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, renk, 3)

        # Sonucu göster
        cv2.imshow("Sonuc", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
