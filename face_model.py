
import cv2
import os
import numpy as np
from PIL import Image


USER_DIR = "dataset/user"
MODEL_PATH = "face_recognizer.yml"

def get_label_map():
    label_map = {}
    for img_name in os.listdir(USER_DIR):
        parts = img_name.split(".")
        if len(parts) >= 3:
            try:
                label = int(parts[1])
                name = parts[0]
                label_map[label] = name
            except ValueError:
                continue
    return label_map

def add_face_image(image_np, name, f_id):
    if not os.path.exists(USER_DIR):
        os.makedirs(USER_DIR)
    sample_count = len([f for f in os.listdir(USER_DIR) if f.startswith(f"{name}.{f_id}.")]) + 1
    img_path = f"{USER_DIR}/{name}.{f_id}.{sample_count}.jpg"
    cv2.imwrite(img_path, image_np)
    return img_path

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

def create_user(f_id, name):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # Set video width
    cam.set(4, 480)  # Set video height
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    user_dir = USER_DIR
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    sample_count = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = faces.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces_detected:
            sample_count += 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite(f"{user_dir}/{name}.{f_id}.{sample_count}.jpg", gray[y:y + h, x:x + w])
            cv2.imshow('Face Capture', frame)
        if cv2.waitKey(100) & 0xFF == ord('q') or sample_count >= 40:
            break
    cam.release()
    cv2.destroyAllWindows()

def train_face_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    user_dir = USER_DIR
    for img_name in os.listdir(user_dir):
        img_path = os.path.join(user_dir, img_name)
        if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        img = Image.open(img_path).convert('L')
        img_np = np.array(img, 'uint8')
        try:
            label = int(img_name.split('.')[1])
        except (IndexError, ValueError):
            print(f"Skipping invalid file name: {img_name}")
            continue
        faces.append(img_np)
        labels.append(label)
    recognizer.train(faces, np.array(labels))
    recognizer.save(MODEL_PATH)
    print("Training complete and model saved as 'face_recognizer.yml'")
    print(f"Total faces trained: {len(np.unique(labels))}")

def recognize_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)
    cam = cv2.VideoCapture(0)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognized_names = []
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = faces.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces_detected:
            face_roi = gray[y:y + h, x:x + w]
            label, confidence = recognizer.predict(face_roi)
            if confidence < 100:
                if label == 1:
                    name = "Robin"
                elif label == 2:
                    name = "Sifat"
                else:
                    name = f"User {label}"
            else:
                name = "Unknown"
            recognized_names.append(name)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    # Return the last recognized name or all names
    return recognized_names[-1] if recognized_names else "Unknown"

if __name__ == "__main__":
    import cv2
    import sys
    print("Face Model Utility")
    print("Usage: python face_model.py [train|recognize] [image_path] [name] [id]")
    if len(sys.argv) < 2:
        print("Specify 'train' to train model or 'recognize' to recognize a face.")
        sys.exit(1)
    mode = sys.argv[1]
    if mode == "train":
        print("Training model...")
        success = train_face_recognizer()
        print("Training success:" if success else "Training failed.")
    elif mode == "recognize":
        if len(sys.argv) < 3:
            print("Provide image path for recognition.")
            sys.exit(1)
        img_path = sys.argv[2]
        img_np = cv2.imread(img_path)
        if img_np is None:
            print("Could not read image.")
            sys.exit(1)
        name = recognize_face(img_np)
        print(f"Recognized Name: {name}")
    elif mode == "add":
        if len(sys.argv) < 5:
            print("Provide image path, name, and id to add face.")
            sys.exit(1)
        img_path = sys.argv[2]
        name = sys.argv[3]
        f_id = int(sys.argv[4])
        img_np = cv2.imread(img_path)
        if img_np is None:
            print("Could not read image.")
            sys.exit(1)
        add_face_image(img_np, name, f_id)
        print(f"Added face for {name} with id {f_id}.")
        train_face_recognizer()
    else:
        print("Unknown mode. Use 'train', 'recognize', or 'add'.")
import cv2
import os
import numpy as np
from PIL import Image

USER_DIR = "dataset/user"
MODEL_PATH = "face_recognizer.yml"


def get_label_map():
    label_map = {}
    for img_name in os.listdir(USER_DIR):
        parts = img_name.split(".")
        if len(parts) >= 3:
            try:
                label = int(parts[1])
                name = parts[0]
                label_map[label] = name
            except ValueError:
                continue
    return label_map

def add_face_image(image_np, name, f_id):
    if not os.path.exists(USER_DIR):
        os.makedirs(USER_DIR)
    sample_count = len([f for f in os.listdir(USER_DIR) if f.startswith(f"{name}.{f_id}.")]) + 1
    img_path = f"{USER_DIR}/{name}.{f_id}.{sample_count}.jpg"
    cv2.imwrite(img_path, image_np)
    return img_path

def train_face_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    for img_name in os.listdir(USER_DIR):
        img_path = os.path.join(USER_DIR, img_name)
        if not img_name.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        try:
            img = Image.open(img_path).convert("L")
            img_np = np.array(img, "uint8")
            label = int(img_name.split(".")[1])
            faces.append(img_np)
            labels.append(label)
        except Exception as e:
            print(f"Error processing {img_name}: {e}")
            continue
    if faces and labels:
        recognizer.train(faces, np.array(labels))
        recognizer.save(MODEL_PATH)
        print("Training complete and model saved.")
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
