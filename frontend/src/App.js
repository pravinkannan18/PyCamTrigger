import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [deviceConnected, setDeviceConnected] = useState(false);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [lastPhoto, setLastPhoto] = useState(null);
  const [connectionType, setConnectionType] = useState('adb');
  const [connectionTypes, setConnectionTypes] = useState([]);
  const [showConnectionModal, setShowConnectionModal] = useState(false);
  const [ipAddress, setIpAddress] = useState('');
  const [port, setPort] = useState('5555');

  // Check device connection on mount
  useEffect(() => {
    checkDeviceConnection();
    loadConnectionTypes();
  }, []);

  const loadConnectionTypes = async () => {
    try {
      const response = await axios.get('/api/connection-types');
      setConnectionTypes(response.data.types);
      setConnectionType(response.data.current);
    } catch (error) {
      console.error('Error loading connection types:', error);
    }
  };

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

  const handleConnectionTypeChange = async (type) => {
    if (type === 'adb_wifi' || type === 'ip_webcam') {
      setConnectionType(type);
      setShowConnectionModal(true);
      setPort(type === 'ip_webcam' ? '8080' : '5555');
    } else {
      setConnectionType(type);
      try {
        await axios.post('/api/set-connection-type', { type });
        setMessage(`Switched to ${type} connection`);
        checkDeviceConnection();
      } catch (error) {
        setMessage('Error changing connection type');
      }
    }
  };

  const handleNetworkConnect = async () => {
    if (!ipAddress) {
      setMessage('Please enter IP address');
      return;
    }

    setLoading(true);
    try {
      let response;
      if (connectionType === 'adb_wifi') {
        response = await axios.post('/api/adb-wifi/connect', {
          ip_address: ipAddress,
          port: parseInt(port)
        });
      } else if (connectionType === 'ip_webcam') {
        response = await axios.post('/api/ip-webcam/connect', {
          ip_address: ipAddress,
          port: parseInt(port)
        });
      }

      if (response.data.success) {
        setMessage(response.data.message);
        setShowConnectionModal(false);
        setDeviceConnected(true);
      } else {
        setMessage('Connection failed: ' + response.data.error);
      }
    } catch (error) {
      setMessage('Error: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📱 Android Camera Controller</h1>
      </header>

      <div className="container">
        <div className="connection-type-selector">
          <label>Connection Method:</label>
          <select 
            value={connectionType} 
            onChange={(e) => handleConnectionTypeChange(e.target.value)}
            disabled={loading}
          >
            {connectionTypes.map(type => (
              <option key={type.value} value={type.value}>
                {type.label} - {type.description}
              </option>
            ))}
          </select>
        </div>

        {showConnectionModal && (
          <div className="modal">
            <div className="modal-content">
              <h3>Connect to {connectionType === 'adb_wifi' ? 'ADB WiFi' : 'IP Webcam'}</h3>
              <div className="form-group">
                <label>Device IP Address:</label>
                <input
                  type="text"
                  placeholder="e.g., 192.168.1.100"
                  value={ipAddress}
                  onChange={(e) => setIpAddress(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Port:</label>
                <input
                  type="text"
                  value={port}
                  onChange={(e) => setPort(e.target.value)}
                />
              </div>
              <div className="modal-actions">
                <button className="btn btn-primary" onClick={handleNetworkConnect} disabled={loading}>
                  {loading ? 'Connecting...' : 'Connect'}
                </button>
                <button className="btn btn-secondary" onClick={() => setShowConnectionModal(false)}>
                  Cancel
                </button>
              </div>
              {connectionType === 'adb_wifi' && (
                <div className="connection-info">
                  <p><strong>Steps for ADB WiFi:</strong></p>
                  <ol>
                    <li>Connect device via USB first</li>
                    <li>Enable TCP/IP mode: <code>adb tcpip 5555</code></li>
                    <li>Find device IP in Settings → About → Status</li>
                    <li>Enter IP address above and connect</li>
                    <li>You can now disconnect USB cable</li>
                  </ol>
                </div>
              )}
              {connectionType === 'ip_webcam' && (
                <div className="connection-info">
                  <p><strong>Steps for IP Webcam:</strong></p>
                  <ol>
                    <li>Install "IP Webcam" app from Play Store</li>
                    <li>Open app and scroll to bottom</li>
                    <li>Tap "Start server"</li>
                    <li>Note the IP address shown (e.g., http://192.168.1.100:8080)</li>
                    <li>Enter IP and port above</li>
                  </ol>
                </div>
              )}
            </div>
          </div>
        )}

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
          <h3>📋 Connection Methods:</h3>
          
          <div className="connection-method">
            <h4>🔌 USB (ADB) - Default</h4>
            <ul>
              <li>Connect device via USB cable</li>
              <li>Enable USB Debugging in Developer Options</li>
              <li>Install ADB on your computer</li>
            </ul>
          </div>

          <div className="connection-method">
            <h4>📶 WiFi (ADB)</h4>
            <ul>
              <li>First connect via USB and enable TCP/IP mode</li>
              <li>Run: <code>adb tcpip 5555</code></li>
              <li>Find device IP address in Settings</li>
              <li>Select "WiFi (ADB)" and enter IP address</li>
              <li>Disconnect USB cable after connected</li>
            </ul>
          </div>

          <div className="connection-method">
            <h4>📹 IP Webcam App</h4>
            <ul>
              <li>Install "IP Webcam" from Play Store</li>
              <li>Open app and start server</li>
              <li>Note the IP address shown</li>
              <li>Select "IP Webcam" and enter IP address</li>
              <li>No USB cable or ADB required!</li>
            </ul>
          </div>

          <div className="connection-method">
            <h4>🖥️ scrcpy - Screen Mirroring</h4>
            <ul>
              <li>Install scrcpy: <a href="https://github.com/Genymobile/scrcpy" target="_blank" rel="noopener noreferrer">Download</a></li>
              <li>Connect via USB or ADB WiFi</li>
              <li>Provides full screen mirroring and control</li>
              <li>Can capture screenshots directly</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
