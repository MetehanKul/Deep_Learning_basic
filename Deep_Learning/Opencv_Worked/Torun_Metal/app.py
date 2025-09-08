import tensorflow as tf
from tensorflow.keras import layers, models , optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.applications import VGG16 , ResNet50 

# Veriyi Hazırlama 
train_datagen = ImageDataGenerator(
    rescale = 1./255,
    rotation_range = 40,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    shear_range = 0.2,
    zoom_range = 0.5,
    horizontal_flip = True,
    fill_mode = 'nearest'
)

train_data = train_datagen.flow_from_directory(
    'dataset/train',
    target_size = (150,150),
    batch_size = 32,
    class_mode = 'binary'
)


test_data = train_datagen.flow_from_directory(
    'dataset/test',
    target_size = (150,150),
    batch_size = 32,
    class_mode = 'binary'
)

# Modeli Oluşturma

## VGG16 Modeli ile Başlama
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
base_model.trainable = False # Önceden eğitilmiş katmanları dondurmaq

for layer in base_model.layers[-4:]:
    layer.trainable = True



# Modelimize yeni katmanlar ekleme
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizers.Adam(learning_rate=1e-5),
    loss = 'binary_crossentropy',
    metrics = ['accuracy'])


# model.compile(
   # optimizers.RMSprop(learning_rate=0.0001),
   # loss = 'binary_crossentropy',
    # metrics = ['accuracy']

# Modeli Eğitme
history = model.fit(
    train_data,
    validation_data = test_data,
    epochs = 10,
    steps_per_epoch = 100,
    validation_steps = 30
)

# Eğitim Sonuçlarını Görselleştirme

accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(accuracy))
plt.plot(epochs, accuracy, 'b', label='Training accuracy')
plt.plot(epochs, val_accuracy, 'r', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'b', label='Training Loss')
plt.plot(epochs, val_loss, 'r', label='Validation Loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()


# Prediction
def predict_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(150, 150))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    if prediction > 0.5:
        print(f"{image_path} : OK")
    else:
        print(f"{image_path} : NOK")

    # Görselleştirme
    plt.imshow(img_array[0])
    plt.axis('off')
    plt.show()


predict_image('dataset/test/NOK/IMG_1129.JPG')

# Görselleştirme
img = tf.keras.preprocessing.image.load_img('dataset/test/NOK/IMG_1130.JPG', target_size=(150, 150))
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0



#ResNet50 Modeli ile Deneme
base_model_resnet = ResNet50(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
base_model_resnet.trainable = False # Önceden eğitilmiş katmanları dondururmaq

# Modelimize yeni katmanlar ekleme
model_resnet = models.Sequential([
    base_model_resnet,
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

model_resnet.compile(
    optimizers.Adam(learning_rate=0.0001),
    loss = 'binary_crossentropy',
    metrics = ['accuracy'])

# Modeli Eğitme
history_resnet = model_resnet.fit(
    train_data,
    validation_data = test_data,
    epochs = 30,
    steps_per_epoch = 100,
    validation_steps = 30
)

# Eğitim Sonuçlarını Görselleştirme
accuracy_resnet = history_resnet.history['accuracy']
val_accuracy_resnet = history_resnet.history['val_accuracy']
loss_resnet = history_resnet.history['loss']
val_loss_resnet = history_resnet.history['val_loss']
epochs_resnet = range(len(accuracy_resnet))
plt.plot(epochs_resnet, accuracy_resnet, 'b', label='Training accuracy')
plt.plot(epochs_resnet, val_accuracy_resnet, 'r', label='Validation accuracy')
plt.title('Training and validation accuracy (ResNet50)')
plt.legend()
plt.figure()
plt.plot(epochs_resnet, loss_resnet, 'b', label='Training Loss')
plt.plot(epochs_resnet, val_loss_resnet, 'r', label='Validation Loss')
plt.title('Training and validation loss (ResNet50)')
plt.legend()
plt.show()

# Prediction with ResNet50 model
def predict_image_resnet(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(150, 150))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model_resnet.predict(img_array)
    if prediction < 0.5:
        print(f"{image_path} : NOK")
    else:
        print(f"{image_path} : OK")

predict_image_resnet('dataset/test/OK/IMG_1064.JPG')

# Görselleştirme
img = tf.keras.preprocessing.image.load_img('dataset/test/NOK/IMG_1130.JPG', target_size=(150, 150))
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0
plt.imshow(img_array[0])
plt.axis('off')
plt.show()