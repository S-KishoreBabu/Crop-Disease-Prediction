import kagglehub
import numpy as np
import os
import cv2
from flask import Flask, request, jsonify, render_template
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = Flask(__name__)

print("Downloading dataset...")
path = kagglehub.dataset_download("mexwell/crop-diseases-classification")
print("Path to dataset files:", path)


data_dir = path
categories = os.listdir(data_dir)

image_size = 128
X = []
y = []

print("Loading dataset...")
for idx, category in enumerate(categories):
    category_path = os.path.join(data_dir, category)
    for img_file in os.listdir(category_path):
        try:
            img_path = os.path.join(category_path, img_file)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (image_size, image_size))
            X.append(img)
            y.append(idx)
        except Exception as e:
            print(f"Error loading image {img_file}: {e}")

X = np.array(X) / 255.0
y = np.array(y)

y = to_categorical(y, num_classes=len(categories))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(image_size, image_size, 3)),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(categories), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

data_gen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

print("Training model...")
history = model.fit(data_gen.flow(X_train, y_train, batch_size=32),
                    validation_data=(X_test, y_test),
                    epochs=10)

print("Evaluating model...")
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

model.save("crop_disease_model.h5")
print("Model saved as crop_disease_model.h5")

model = load_model("crop_disease_model.h5")

def predict_disease(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (image_size, image_size))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    return categories[predicted_class]

# Flask route for prediction
@app.route('/')
def index():
    return render_template('scanner.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"})

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    prediction = predict_disease(filepath)
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
