# Face Recognition CV Project

## Overview
This project is a face recognition system built with Python and Flask for the backend, and Next.js for the frontend. It allows users to add face images, train a face recognizer, and recognize faces from images or camera input. The backend uses OpenCV for image processing and face recognition, and stores user images in the `dataset/user` directory.

## Features
- Add new user faces via API
- Train face recognizer model
- Recognize faces from images
- RESTful API endpoints
- Next.js frontend for user interaction

## Installation

### 1. Clone the repository
```
git clone <your-repo-url>
cd face_recognition_cv-1
```

### 2. Install Python dependencies
Make sure you have Python 3.8+ installed.
Install all required packages:
```
pip install -r requirements.txt
```

### 3. Install Node.js dependencies (for frontend)
Navigate to the `app` directory and install dependencies:
```
cd app
npm install
```

## Usage

### 1. Run the backend server
From the project root:
```
python face_backend.py
```
The server will start at `http://0.0.0.0:5000`.

### 2. Run the frontend (Next.js)
From the `app` directory:
```
npm run dev
```
The frontend will start at `http://localhost:3000`.

## API Endpoints
- `POST /add-face` — Add a new face image
- `POST /recognize` — Recognize a face from an image
- `GET /recognize-camera` — Recognize face from camera (if implemented)
- `POST /add-face-camera` — Add face from camera (if implemented)

## Dataset
User face images are stored in `dataset/user/` as `.jpg` files. Each user has a unique ID and name.

## Notes
- Make sure your webcam is accessible if using camera endpoints.
- The backend must be running for the frontend to interact with it.

## License
MIT
