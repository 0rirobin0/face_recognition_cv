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
  const [loading, setLoading] = useState<boolean>(false);

  const startCamera = async () => {
    if (navigator.mediaDevices && videoRef.current) {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      setIsCameraOn(true);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsCameraOn(false);
    }
  };

  const captureImage = (): string | null => {
    if (!videoRef.current) return null;
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx?.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
  };

  const handleAddFace = async () => {
    if (!newFaceName) return alert('Enter a name first!');
    if (!videoRef.current) return alert('Camera not started!');

    setLoading(true);
    const images: string[] = [];

    for (let i = 0; i < 100; i++) {
      const imageData = captureImage();
      if (imageData) images.push(imageData);
      await new Promise(r => setTimeout(r, 100)); // ~10 fps
    }

    try {
      const res = await fetch('http://127.0.0.1:5000/add-face', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newFaceName, images }),
      });
      const data = await res.json();
      if (data.success) {
        alert(`Face for ${newFaceName} added successfully!`);
        setNewFaceName('');
      } else {
        alert('Failed to add face: ' + data.error);
      }
    } catch (err) {
      console.error(err);
      alert('Error adding face!');
    } finally {
      setLoading(false);
    }
  };

  const handleRecognize = async () => {
    const imageData = captureImage();
    if (!imageData) return alert('Failed to capture image!');
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:5000/recognize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData }),
      });
      const data = await res.json();
      if (data.success) setRecognizedName(data.name);
      else alert('Recognition failed: ' + data.error);
    } catch (err) {
      console.error(err);
      alert('Error recognizing face!');
    } finally {
      setLoading(false);
    }
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

      <div className="flex gap-3 mb-6">
        <button onClick={startCamera} disabled={isCameraOn} className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md disabled:opacity-50">
          <Camera size={18} /> Start
        </button>
        <button onClick={stopCamera} disabled={!isCameraOn} className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded-xl shadow-md disabled:opacity-50">
          <StopCircle size={18} /> Stop
        </button>
        <button onClick={() => setMode('recognize')} className={`flex items-center gap-2 px-4 py-2 rounded-xl shadow-md ${mode === 'recognize' ? 'bg-green-600 text-white' : 'bg-gray-600 hover:bg-gray-700'}`}>
          <ScanFace size={18} /> Recognize
        </button>
        <button onClick={() => setMode('add')} className={`flex items-center gap-2 px-4 py-2 rounded-xl shadow-md ${mode === 'add' ? 'bg-yellow-600 text-white' : 'bg-gray-600 hover:bg-gray-700'}`}>
          <UserPlus size={18} /> Add Face
        </button>
      </div>

      <motion.div className="relative w-[480px] h-[360px] rounded-2xl overflow-hidden shadow-lg border-2 border-gray-700" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}>
        <video ref={videoRef} autoPlay className="w-full h-full object-cover bg-black" />
      </motion.div>

      {mode === 'recognize' && (
        <motion.div className="mt-6 flex flex-col items-center">
          <button onClick={handleRecognize} className="px-5 py-2 bg-green-600 hover:bg-green-700 rounded-xl shadow-md" disabled={loading}>
            Recognize Face
          </button>
          {loading && <div className="mt-4"><img src="/spinner.svg" alt="Loading..." className="w-12 h-12 animate-spin" /></div>}
          <div className="mt-4 text-lg">
            Recognized Name: <span className="font-bold text-green-400">{recognizedName}</span>
          </div>
        </motion.div>
      )}

      {mode === 'add' && (
        <motion.div className="mt-6 flex flex-col items-center">
          <input type="text" placeholder="Enter Name" value={newFaceName} onChange={e => setNewFaceName(e.target.value)} className="mb-3 px-3 py-2 rounded-xl text-black w-64 border focus:outline-none focus:ring-2 focus:ring-yellow-500" />
          <button onClick={handleAddFace} className="px-5 py-2 bg-yellow-600 hover:bg-yellow-700 rounded-xl shadow-md" disabled={loading}>
            Add Face
          </button>
          {loading && <div className="mt-4"><img src="/spinner.svg" alt="Loading..." className="w-12 h-12 animate-spin" /></div>}
        </motion.div>
      )}
    </div>
  );
}
