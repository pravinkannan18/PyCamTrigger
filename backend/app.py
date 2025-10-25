from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from camera_controller import CameraController
import os

app = Flask(__name__)
CORS(app)

camera = CameraController()

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
