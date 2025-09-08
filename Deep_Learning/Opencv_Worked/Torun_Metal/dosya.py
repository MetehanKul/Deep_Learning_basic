## Yapılacaklar 
# 1. Dosya açma ve okuma
# 2. Dosyayı okuduktan sonra opencv ile gösterme
# 3. Dosyayı okuduktan sonra matplotlib ile gösterme
# açılan dosyada opencv ile çizim yapma
# 

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

# Dosya açma ve okuma
file_path = 'dataset/test/OK/1.jpg'  # Dosya yolu
if not os.path.exists(file_path):
    print(f"Dosya bulunamadı: {file_path}")
    exit()
image = cv2.imread(file_path)
if image is None:
    print("Dosya okunamadı veya geçersiz format.")
    exit()
print("Dosya başarıyla okundu.")
print(f"Resim boyutu: {image.shape}")
print(f"Resim veri tipi: {image.dtype}")
print(f"Resim min değeri: {np.min(image)}")
print(f"Resim max değeri: {np.max(image)}")
print(f"Resim ortalama değeri: {np.mean(image)}")
print(f"Resim standart sapması: {np.std(image)}")
print(f"Resim medyan değeri: {np.median(image)}")
print(f"Resim varyans değeri: {np.var(image)}")
print(f"Resim toplam değeri: {np.sum(image)}")
print(f"Resim şekli: {image.shape}")

# Dosyayı okuduktan sonra opencv ile gösterme
cv2.imshow('OpenCV Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Dosyayı okuduktan sonra matplotlib ile gösterme
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR to RGB
plt.imshow(image_rgb)
plt.axis('off')  # Eksenleri kapat
plt.show()

# Açılan dosyada opencv ile çizim yapma
image_copy = image.copy()
cv2.circle(image_copy, (100, 100), 50, (0, 255, 0), 5)  # Yeşil daire çiz
cv2.rectangle(image_copy, (200, 200), (300, 300), (255, 0, 0), 3)  # Mavi kare çiz
cv2.line(image_copy, (400, 400), (500, 500), (0, 0, 255), 2)  # Kırmızı çizgi çiz
cv2.putText(image_copy, 'OpenCV', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # Beyaz metin ekle
cv2.imshow('Drawn Image', image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Açılan dosyada matplotlib ile çizim yapma
fig, ax = plt.subplots()
ax.imshow(image_rgb)
circle = plt.Circle((100, 100), 50, color='green', fill=False, linewidth=5)
ax.add_patch(circle)
rectangle = plt.Rectangle((200, 200), 100, 100, color='blue', fill=False, linewidth=3)
ax.add_patch(rectangle)
line = plt.Line2D((400, 500), (400, 500), color='red', linewidth=2)
ax.add_line(line)
ax.text(50, 400, 'Matplotlib', color='white', fontsize=12)
plt.axis('off')  # Eksenleri kapat
plt.show()
# Dosyayı kaydetme