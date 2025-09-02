from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np
import base64
from face_model import train_face_recognizer, recognize_face

app = Flask(__name__)
CORS(app)

FACES_DIR = "faces"
os.makedirs(FACES_DIR, exist_ok=True)


def save_images(name, images):
    user_folder = os.path.join(FACES_DIR, name)
    os.makedirs(user_folder, exist_ok=True)
    for idx, image_data in enumerate(images, start=1):
        try:
            if ',' in image_data:
                _, encoded = image_data.split(',', 1)
            else:
                encoded = image_data
            img_bytes = base64.b64decode(encoded)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img_np is not None:
                cv2.imwrite(os.path.join(user_folder, f"{name}_{idx}.jpg"), img_np)
        except Exception as e:
            print(f"Error saving frame {idx}: {e}")


@app.route("/add-face", methods=["POST"])
def add_face():
    data = request.get_json()
    name = data.get("name")
    images = data.get("images")
    if not name or not images:
        return jsonify({"success": False, "error": "Missing name or images"}), 400

    try:
        save_images(name, images)
        train_face_recognizer()  # retrain after adding new images
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error adding face: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/recognize", methods=["POST"])
def recognize():
    data = request.get_json()
    image_data = data.get("image")
    if not image_data:
        return jsonify({"success": False, "error": "Missing image"}), 400

    try:
        if ',' in image_data:
            _, encoded = image_data.split(',', 1)
        else:
            encoded = image_data
        img_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_np is None:
            raise ValueError("Failed to decode image")
    except Exception as e:
        print(f"Error decoding image: {e}")
        return jsonify({"success": False, "error": "Invalid image"}), 400

    try:
        name = recognize_face(img_np)
        return jsonify({"success": True, "name": name})
    except Exception as e:
        print(f"Error recognizing face: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
