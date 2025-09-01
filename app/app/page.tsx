'use client';
import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Camera, StopCircle, UserPlus, ScanFace } from 'lucide-react';

export default function Home() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [recognizedName, setRecognizedName] = useState<string>('');
  const [newFaceName, setNewFaceName] = useState<string>('');
  const [mode, setMode] = useState<'recognize' | 'add'>('recognize');
  const [isCameraOn, setIsCameraOn] = useState<boolean>(false);

  // Start camera
  const startCamera = async () => {
    if (navigator.mediaDevices && videoRef.current) {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      setIsCameraOn(true);
    }
  };

  // Stop camera
  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsCameraOn(false);
    }
  };

  // Capture image from video
  const captureImage = () => {
    if (!videoRef.current) return null;
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx?.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
  };

  // Add new face using backend webcam
  const handleAddFaceCamera = async () => {
    if (!newFaceName) {
      alert('Please enter a name first.');
      return;
    }
    await fetch('http://127.0.0.1:5000/add-face-camera', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newFaceName, id: 1 }),
    });
    alert(`Face for ${newFaceName} added and model updated!`);
    setNewFaceName('');
  };

  // Real-time face recognition using backend webcam
  const handleRecognizeCamera = async () => {
    await fetch('http://127.0.0.1:5000/recognize-camera', {
      method: 'GET',
    });
    // Recognition result will be shown in backend window
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-6">
      <motion.h1
        className="text-4xl font-bold mb-6 text-center"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
      >
        AI Face Recognition System
      </motion.h1>

      {/* Controls */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={startCamera}
          disabled={isCameraOn}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md disabled:opacity-50"
        >
          <Camera size={18} /> Start
        </button>
        <button
          onClick={stopCamera}
          disabled={!isCameraOn}
          className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-xl shadow-md disabled:opacity-50"
        >
          <StopCircle size={18} /> Stop
        </button>
        <button
          onClick={() => setMode('recognize')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl shadow-md ${
            mode === 'recognize'
              ? 'bg-green-600 text-white'
              : 'bg-gray-600 hover:bg-gray-700'
          }`}
        >
          <ScanFace size={18} /> Recognize
        </button>
        <button
          onClick={() => setMode('add')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl shadow-md ${
            mode === 'add'
              ? 'bg-yellow-600 text-white'
              : 'bg-gray-600 hover:bg-gray-700'
          }`}
        >
          <UserPlus size={18} /> Add Face
        </button>
      </div>

      {/* Video Box */}
      <motion.div
        className="relative w-[480px] h-[360px] rounded-2xl overflow-hidden shadow-lg border-2 border-gray-700"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
      >
        <video ref={videoRef} autoPlay className="w-full h-full object-cover bg-black" />
      </motion.div>

      {/* Modes */}
      {mode === 'recognize' && (
        <motion.div
          className="mt-6 flex flex-col items-center"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <button
            onClick={handleRecognizeCamera}
            className="px-5 py-2 bg-green-600 hover:bg-green-700 rounded-xl shadow-md"
          >
            Recognize Face Using Backend Camera
          </button>
          <div className="mt-4 text-lg">
            Recognized Name:{' '}
            <span className="font-bold text-green-400">{recognizedName}</span>
          </div>
        </motion.div>
      )}

      {mode === 'add' && (
        <motion.div
          className="mt-6 flex flex-col items-center"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <input
            type="text"
            placeholder="Enter Name"
            value={newFaceName}
            onChange={e => setNewFaceName(e.target.value)}
            className="mb-3 px-3 py-2 rounded-xl text-black w-64 border focus:outline-none focus:ring-2 focus:ring-yellow-500"
          />
          <button
            onClick={handleAddFaceCamera}
            className="px-5 py-2 bg-yellow-600 hover:bg-yellow-700 rounded-xl shadow-md"
          >
            Add Face Using Backend Camera
          </button>
        </motion.div>
      )}
    </div>
  );
}
