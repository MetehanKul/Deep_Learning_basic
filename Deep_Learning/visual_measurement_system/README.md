# Visual Measurement System

**Visual Measurement System**, fotoğraflar veya kamera görüntüleri üzerinden nesne ölçümü yapmayı sağlayan bir masaüstü uygulamasıdır. Sistem, kullanıcıdan iki nokta seçmesini ister ve bu noktalar arasındaki gerçek mesafe ile kalibrasyon yapar. Kalibrasyon tamamlandıktan sonra, ister yüklenen görsellerde ister canlı kamera görüntüsünde, nesnelerin boyutlarını otomatik olarak ölçer ve tolerans kontrolü gerçekleştirir.

---

## Temel Özellikler

- **Kalibrasyon:** Görsel üzerinde iki nokta seçilerek gerçek mesafe girilir ve sistem milimetre/piksel oranını hesaplar.
- **Görsel Yükleme:** Bilgisayardan fotoğraf seçip ölçüm yapılabilir.
- **Gerçek Zamanlı Kamera:** Kamera ile canlı görüntü alınabilir ve anlık ölçüm yapılabilir.
- **Otomatik Ölçüm:** Parçanın boy, genişlik ve çap gibi ölçüleri otomatik olarak hesaplanır.
- **Tolerans Kontrolü:** Ölçülen değerler, teknik resim ölçüleriyle karşılaştırılır ve uygunluk durumu görsel olarak gösterilir.
- **Kullanıcı Dostu Arayüz:** PyQt5 tabanlı, kolay kullanımlı masaüstü arayüz.

---

## Kullanım Senaryosu

1. **Kalibrasyon Yap:** Görüntü üzerinde iki nokta seçin ve aralarındaki gerçek mesafeyi girin.
2. **Otomatik Ölçüm:** Sistem, seçilen nesnenin boyutlarını otomatik olarak hesaplar ve ekranda gösterir.
3. **Tolerans Kontrolü:** Ölçülen değerler, önceden belirlenen teknik resim ölçüleriyle karşılaştırılır ve uygunluk durumu renkli olarak belirtilir.
4. **Son Nokta** Parça üzerinde ölçülen değerler teknik resim ile uyuşuyorsa parçaya 'OK' uyuşmuyorsa 'NOK' uyarısı verecek.

---

## Klasör Yapısı

```
visual_measurement_system/
│
├── assets/                # Örnek görseller ve kalibrasyon dosyaları
├── calibrate.py           # Kalibrasyon işlemleri için modül
├── camera_thread.py       # Kamera akışını yöneten thread
├── db.py                  # Ölçüm ve parça veritabanı işlemleri
├── main.py                # Ana uygulama dosyası (PyQt5 arayüzü)
├── measurement.py         # Görüntüden ölçüm çıkarımı yapan fonksiyonlar
├── utils.py               # Yardımcı fonksiyonlar (görsel yükleme vb.)
├── requirements.txt       # Gerekli Python paketleri
└── README.md              # Proje açıklaması (bu dosya)
```

---

## Kurulum

1. **Gereksinimleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Uygulamayı başlatın:**
    ```bash
    python main.py
    ```

---

## Kullanılan Teknolojiler

- Python 3.x
- OpenCV
- PyQt5
- NumPy

---

## Notlar

- Görsel yüklerken dosya yolunda Türkçe karakter veya boşluk olmamasına dikkat edin.
- Kalibrasyon için görüntü üzerinde iki nokta seçip, gerçek uzunluğu (mm) girmeniz gerekir.

---

## Katkı

Katkıda bulunmak için lütfen bir pull request gönderin veya issue açın.

---