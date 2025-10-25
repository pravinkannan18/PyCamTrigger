import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [deviceConnected, setDeviceConnected] = useState(false);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [photos, setPhotos] = useState([]);
  const [lastPhoto, setLastPhoto] = useState(null);

  // Check device connection on mount
  useEffect(() => {
    checkDeviceConnection();
  }, []);

  const checkDeviceConnection = async () => {
    try {
      const response = await axios.get('/api/check-device');
      setDeviceConnected(response.data.connected);
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error connecting to backend server');
      console.error(error);
    }
  };

  const handleStartCamera = async () => {
    setLoading(true);
    setMessage('Opening camera...');
    
    try {
      const response = await axios.post('/api/open-camera');
      
      if (response.data.success) {
        setCameraOpen(true);
        setMessage('Camera opened! You can now capture photos.');
      } else {
        setMessage('Failed to open camera: ' + response.data.message);
      }
    } catch (error) {
      setMessage('Error: ' + (error.response?.data?.error || error.message));
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCapturePhoto = async () => {
    setLoading(true);
    setMessage('Capturing photo...');
    
    try {
      const response = await axios.post('/api/capture-photo');
      
      if (response.data.success) {
        setMessage('Photo captured successfully!');
        setLastPhoto(response.data.filename);
        loadPhotos(); // Refresh photo list
      } else {
        setMessage('Failed to capture photo: ' + response.data.error);
      }
    } catch (error) {
      setMessage('Error: ' + (error.response?.data?.error || error.message));
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const loadPhotos = async () => {
    try {
      const response = await axios.get('/api/photos');
      setPhotos(response.data.photos);
    } catch (error) {
      console.error('Error loading photos:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📱 Android Camera Controller</h1>
      </header>

      <div className="container">
        <div className="status-section">
          <div className={`status-indicator ${deviceConnected ? 'connected' : 'disconnected'}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {deviceConnected ? 'Device Connected' : 'Device Not Connected'}
            </span>
          </div>
          <button 
            className="btn btn-secondary"
            onClick={checkDeviceConnection}
            disabled={loading}
          >
            🔄 Refresh Connection
          </button>
        </div>

        {message && (
          <div className={`message ${deviceConnected ? 'success' : 'warning'}`}>
            {message}
          </div>
        )}

        <div className="controls">
          <button
            className="btn btn-primary btn-large"
            onClick={handleStartCamera}
            disabled={!deviceConnected || loading || cameraOpen}
          >
            {loading && !cameraOpen ? '⏳ Opening...' : '📷 Start Camera'}
          </button>

          {cameraOpen && (
            <button
              className="btn btn-success btn-large"
              onClick={handleCapturePhoto}
              disabled={loading}
            >
              {loading ? '⏳ Capturing...' : '📸 Capture Photo'}
            </button>
          )}
        </div>

        {lastPhoto && (
          <div className="photo-preview">
            <h3>Latest Capture:</h3>
            <img 
              src={`/api/photos/${lastPhoto}`} 
              alt="Captured" 
              className="preview-image"
            />
            <p className="photo-name">{lastPhoto}</p>
          </div>
        )}

        <div className="instructions">
          <h3>📋 Setup Instructions:</h3>
          <ol>
            <li>Connect your Android device via USB cable</li>
            <li>Enable "USB Debugging" in Developer Options</li>
            <li>Install ADB (Android Debug Bridge) on your computer</li>
            <li>Click "Start Camera" to open the camera app</li>
            <li>Click "Capture Photo" to take a picture</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default App;
