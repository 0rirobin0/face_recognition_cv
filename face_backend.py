
from flask import Flask, request, jsonify
import base64
import numpy as np
import cv2
import os
from face_model import train_face_recognizer, create_user, recognize_faces, add_face_image, recognize_face

app = Flask(__name__)

@app.route('/add-face-camera', methods=['POST'])
def add_face_camera():
	data = request.get_json()
	name = data.get('name')
	f_id = data.get('id', 1)
	create_user(f_id, name)
	train_face_recognizer()
	return jsonify({'success': True})

@app.route('/recognize-camera', methods=['GET'])
def recognize_camera():
	name = recognize_faces()
	return jsonify({'name': name})

@app.route('/recognize', methods=['POST'])
def recognize():
	data = request.get_json()
	image_data = data['image']
	header, encoded = image_data.split(',', 1)
	img_bytes = base64.b64decode(encoded)
	nparr = np.frombuffer(img_bytes, np.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	name = recognize_face(img_np)
	return jsonify({'name': name})

@app.route('/add-face', methods=['POST'])
def add_face_route():
	data = request.get_json()
	image_data = data['image']
	name = data['name']
	header, encoded = image_data.split(',', 1)
	img_bytes = base64.b64decode(encoded)
	nparr = np.frombuffer(img_bytes, np.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	# Assign a new ID for the user (max existing + 1)
	user_dir = "dataset/user"
	existing_ids = []
	for img_file in os.listdir(user_dir):
		try:
			existing_ids.append(int(img_file.split('.')[1]))
		except:
			pass
	new_id = max(existing_ids) + 1 if existing_ids else 1
	add_face_image(img_np, name, new_id)
	train_face_recognizer()
	return jsonify({'success': True})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
