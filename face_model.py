import cv2
import os
import numpy as np
from PIL import Image

FACES_DIR = "faces"
MODEL_PATH = "face_recognizer.yml"


def get_label_map():
    label_map = {}
    if not os.path.exists(FACES_DIR):
        return label_map
    for idx, name in enumerate(os.listdir(FACES_DIR)):
        label_map[idx] = name
    return label_map


def train_face_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []

    if not os.path.exists(FACES_DIR):
        return False

    label_map = {}
    for idx, name in enumerate(os.listdir(FACES_DIR)):
        user_folder = os.path.join(FACES_DIR, name)
        if not os.path.isdir(user_folder):
            continue
        label_map[idx] = name
        # Iterate through ALL images in this user's folder
        for img_file in os.listdir(user_folder):
            if not img_file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            try:
                img_path = os.path.join(user_folder, img_file)
                img = Image.open(img_path).convert("L")
                img_np = np.array(img, "uint8")
                faces.append(img_np)
                labels.append(idx)
            except Exception as e:
                print(f"Error processing {img_file}: {e}")
                continue

    if faces and labels:
        recognizer.train(faces, np.array(labels))
        recognizer.save(MODEL_PATH)
        print(f"Training complete. {len(set(labels))} users trained, total images: {len(faces)}")
        return True

    print("No faces found for training.")
    return False


def recognize_face(image_np):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.exists(MODEL_PATH):
        return "Unknown"
    recognizer.read(MODEL_PATH)
    label_map = get_label_map()

    faces_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces_detected = faces_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces_detected:
        face_roi = gray[y:y + h, x:x + w]
        try:
            label, confidence = recognizer.predict(face_roi)
            if confidence < 100:
                return label_map.get(label, f"User {label}")
            else:
                return "Unknown"
        except Exception as e:
            print(f"Recognition error: {e}")
            return "Error"
    return "No Face Found"
