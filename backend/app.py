from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from camera_controller import CameraController
import os

app = Flask(__name__)
CORS(app)

camera = CameraController()

# ==================== Connection Management ====================

@app.route('/api/connection-types', methods=['GET'])
def get_connection_types():
    """Get available connection types"""
    return jsonify({
        'types': [
            {'value': 'adb', 'label': 'USB (ADB)', 'description': 'Connect via USB cable with ADB'},
            {'value': 'adb_wifi', 'label': 'WiFi (ADB)', 'description': 'Connect via WiFi using ADB'},
            {'value': 'ip_webcam', 'label': 'IP Webcam', 'description': 'Use IP Webcam Android app'},
            {'value': 'scrcpy', 'label': 'scrcpy', 'description': 'Screen mirroring with scrcpy'}
        ],
        'current': camera.connection_type
    })

@app.route('/api/set-connection-type', methods=['POST'])
def set_connection_type():
    """Set connection type"""
    data = request.json
    conn_type = data.get('type')
    result = camera.set_connection_type(conn_type, **data)
    return jsonify(result)

@app.route('/api/connection-info', methods=['GET'])
def get_connection_info():
    """Get current connection information"""
    info = camera.get_connection_info()
    return jsonify(info)

# ==================== ADB WiFi ====================

@app.route('/api/adb-wifi/setup-tcpip', methods=['POST'])
def setup_adb_tcpip():
    """Enable TCP/IP mode (must be USB connected first)"""
    data = request.json
    port = data.get('port', 5555)
    result = camera.setup_adb_tcpip(port)
    return jsonify(result)

@app.route('/api/adb-wifi/connect', methods=['POST'])
def connect_adb_wifi():
    """Connect via ADB over WiFi"""
    data = request.json
    ip_address = data.get('ip_address')
    port = data.get('port', 5555)
    
    if not ip_address:
        return jsonify({'success': False, 'error': 'IP address required'}), 400
    
    result = camera.connect_adb_wifi(ip_address, port)
    return jsonify(result)

@app.route('/api/adb-wifi/disconnect', methods=['POST'])
def disconnect_adb_wifi():
    """Disconnect ADB WiFi"""
    result = camera.disconnect_adb_wifi()
    return jsonify(result)

# ==================== IP Webcam ====================

@app.route('/api/ip-webcam/connect', methods=['POST'])
def connect_ip_webcam():
    """Connect to IP Webcam app"""
    data = request.json
    ip_address = data.get('ip_address')
    port = data.get('port', 8080)
    
    if not ip_address:
        return jsonify({'success': False, 'error': 'IP address required'}), 400
    
    result = camera.connect_ip_webcam(ip_address, port)
    return jsonify(result)

@app.route('/api/ip-webcam/video-url', methods=['GET'])
def get_ip_webcam_video_url():
    """Get IP Webcam video stream URL"""
    url = camera.get_ip_webcam_video_url()
    return jsonify({'video_url': url})

# ==================== scrcpy ====================

@app.route('/api/scrcpy/check', methods=['GET'])
def check_scrcpy():
    """Check if scrcpy is installed"""
    result = camera.check_scrcpy_installed()
    return jsonify(result)

@app.route('/api/scrcpy/start', methods=['POST'])
def start_scrcpy():
    """Start scrcpy"""
    data = request.json or {}
    options = data.get('options', {})
    result = camera.start_scrcpy(options)
    return jsonify(result)

# ==================== Device & Camera Operations ====================

@app.route('/api/check-device', methods=['GET'])
def check_device():
    """Check if Android device is connected"""
    is_connected = camera.check_device_connection()
    return jsonify({
        'connected': is_connected,
        'message': 'Device connected' if is_connected else 'No device found. Please connect your Android device via USB and enable USB debugging.'
    })

@app.route('/api/open-camera', methods=['POST'])
def open_camera():
    """Open camera on Android device"""
    if not camera.check_device_connection():
        return jsonify({
            'success': False,
            'error': 'No device connected'
        }), 400
    
    success = camera.open_camera()
    return jsonify({
        'success': success,
        'message': 'Camera opened successfully' if success else 'Failed to open camera'
    })

@app.route('/api/capture-photo', methods=['POST'])
def capture_photo():
    """Capture a photo from Android camera"""
    if not camera.check_device_connection():
        return jsonify({
            'success': False,
            'error': 'No device connected'
        }), 400
    
    result = camera.capture_photo()
    return jsonify(result)

@app.route('/api/photos', methods=['GET'])
def get_photos():
    """Get list of captured photos"""
    photos = camera.get_captured_photos()
    return jsonify({
        'photos': [photo['filename'] for photo in photos]
    })

@app.route('/api/photos/<filename>', methods=['GET'])
def get_photo(filename):
    """Serve a specific photo"""
    photos_dir = camera.photos_dir
    return send_from_directory(photos_dir, filename)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Make sure:")
    print("1. Android device is connected via USB")
    print("2. USB debugging is enabled")
    print("3. ADB is installed and in PATH")
    app.run(debug=True, host='0.0.0.0', port=5000)
