import subprocess
import os
import requests
from datetime import datetime
import json

class CameraController:
    def __init__(self):
        self.photos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'captured_photos')
        os.makedirs(self.photos_dir, exist_ok=True)
        self.connection_type = 'adb'  # Options: 'adb', 'ip_webcam', 'scrcpy', 'adb_wifi'
        self.ip_webcam_url = None
        self.device_ip = None
        
    # ==================== Connection Type Management ====================
    
    def set_connection_type(self, conn_type, **kwargs):
        """Set the connection type and related parameters"""
        if conn_type in ['adb', 'ip_webcam', 'scrcpy', 'adb_wifi']:
            self.connection_type = conn_type
            
            if conn_type == 'ip_webcam':
                ip = kwargs.get('ip_address')
                port = kwargs.get('port', 8080)
                if ip:
                    self.ip_webcam_url = f'http://{ip}:{port}'
            
            if conn_type == 'adb_wifi':
                self.device_ip = kwargs.get('ip_address')
            
            return {'success': True, 'connection_type': conn_type}
        return {'success': False, 'error': 'Invalid connection type'}
    
    def get_connection_info(self):
        """Get current connection information"""
        return {
            'type': self.connection_type,
            'ip_webcam_url': self.ip_webcam_url,
            'device_ip': self.device_ip
        }
    
    # ==================== ADB USB Connection ====================
        
    def check_device_connection(self):
        """Check device connection based on current connection type"""
        if self.connection_type == 'adb' or self.connection_type == 'adb_wifi' or self.connection_type == 'scrcpy':
            return self.check_adb_connection()
        elif self.connection_type == 'ip_webcam':
            return self.check_ip_webcam_connection()
        return False
    
    def check_adb_connection(self):
        """Check if Android device is connected via ADB (USB or WiFi)"""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            devices = result.stdout.strip().split('\n')[1:]
            connected_devices = [d for d in devices if d.strip() and 'device' in d]
            return len(connected_devices) > 0
        except Exception as e:
            print(f"Error checking ADB device: {e}")
            return False
    
    # ==================== ADB WiFi Connection ====================
    
    def connect_adb_wifi(self, ip_address, port=5555):
        """Connect to Android device via WiFi using ADB"""
        try:
            self.device_ip = ip_address
            
            # Connect to device over WiFi
            result = subprocess.run(
                ['adb', 'connect', f'{ip_address}:{port}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if 'connected' in result.stdout.lower():
                self.connection_type = 'adb_wifi'
                return {'success': True, 'message': f'Connected to {ip_address}:{port}'}
            else:
                return {'success': False, 'error': 'Failed to connect via WiFi', 'output': result.stdout}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def setup_adb_tcpip(self, port=5555):
        """Enable TCP/IP mode on USB-connected device (required before WiFi connection)"""
        try:
            result = subprocess.run(
                ['adb', 'tcpip', str(port)],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {'success': True, 'message': f'ADB listening on port {port}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def disconnect_adb_wifi(self):
        """Disconnect ADB WiFi connection"""
        try:
            subprocess.run(['adb', 'disconnect'], timeout=5)
            self.device_ip = None
            return {'success': True, 'message': 'Disconnected'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== IP Webcam Methods ====================
    
    def check_ip_webcam_connection(self):
        """Check if IP Webcam app is accessible"""
        try:
            if not self.ip_webcam_url:
                return False
            response = requests.get(f'{self.ip_webcam_url}/status.json', timeout=3)
            return response.status_code == 200
        except Exception as e:
            print(f"Error connecting to IP Webcam: {e}")
            return False
    
    def connect_ip_webcam(self, ip_address, port=8080):
        """Connect to IP Webcam app"""
        try:
            url = f'http://{ip_address}:{port}'
            response = requests.get(f'{url}/status.json', timeout=5)
            
            if response.status_code == 200:
                self.ip_webcam_url = url
                self.connection_type = 'ip_webcam'
                return {'success': True, 'message': f'Connected to IP Webcam at {url}'}
            return {'success': False, 'error': 'IP Webcam not responding'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_ip_webcam_video_url(self):
        """Get video stream URL from IP Webcam"""
        if self.ip_webcam_url:
            return f'{self.ip_webcam_url}/video'
        return None
    
    def capture_photo_ip_webcam(self):
        """Capture photo from IP Webcam app"""
        try:
            if not self.ip_webcam_url:
                return {'success': False, 'error': 'IP Webcam not connected'}
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            local_path = os.path.join(self.photos_dir, f'photo_{timestamp}.jpg')
            
            # Get photo from IP Webcam
            photo_url = f'{self.ip_webcam_url}/photo.jpg'
            response = requests.get(photo_url, timeout=10)
            
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                return {
                    'success': True,
                    'filename': f'photo_{timestamp}.jpg',
                    'path': local_path,
                    'method': 'ip_webcam'
                }
            
            return {'success': False, 'error': 'Failed to capture photo'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== scrcpy Methods ====================
    
    def check_scrcpy_installed(self):
        """Check if scrcpy is installed"""
        try:
            result = subprocess.run(
                ['scrcpy', '--version'],
                capture_output=True,
                timeout=5
            )
            return {'installed': result.returncode == 0, 'version': result.stdout.decode() if result.returncode == 0 else None}
        except Exception as e:
            return {'installed': False, 'error': str(e)}
    
    def start_scrcpy(self, options=None):
        """Start scrcpy for screen mirroring"""
        try:
            cmd = ['scrcpy']
            
            # Add optional parameters
            if options:
                if options.get('no_control'):
                    cmd.append('--no-control')
                if options.get('turn_screen_off'):
                    cmd.append('--turn-screen-off')
                if options.get('stay_awake'):
                    cmd.append('--stay-awake')
            
            # Start scrcpy in background
            subprocess.Popen(cmd)
            self.connection_type = 'scrcpy'
            
            return {'success': True, 'message': 'scrcpy started'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def capture_screenshot_scrcpy(self):
        """Capture screenshot using ADB (works with scrcpy)"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            remote_path = f'/sdcard/Pictures/screenshot_{timestamp}.png'
            local_path = os.path.join(self.photos_dir, f'screenshot_{timestamp}.png')
            
            # Take screenshot using ADB
            subprocess.run([
                'adb', 'shell',
                'screencap', '-p', remote_path
            ], check=True, timeout=10)
            
            # Pull screenshot
            subprocess.run([
                'adb', 'pull',
                remote_path,
                local_path
            ], check=True, timeout=30)
            
            # Delete remote screenshot
            subprocess.run([
                'adb', 'shell',
                'rm', remote_path
            ], timeout=5)
            
            return {
                'success': True,
                'filename': f'screenshot_{timestamp}.png',
                'path': local_path,
                'method': 'scrcpy_screenshot'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== Camera Operations ====================
    # ==================== Camera Operations ====================
    
    def open_camera(self):
        """Open camera based on connection type"""
        if self.connection_type in ['adb', 'adb_wifi', 'scrcpy']:
            return self.open_camera_adb()
        elif self.connection_type == 'ip_webcam':
            # IP Webcam app IS the camera - already running
            return True
        return False
    
    def open_camera_adb(self):
        """Open the camera app on Android device via ADB"""
        try:
            # Open camera using ADB
            subprocess.run([
                'adb', 'shell', 
                'am', 'start', 
                '-a', 'android.media.action.IMAGE_CAPTURE'
            ], check=True, timeout=10)
            return True
        except subprocess.TimeoutExpired:
            print("Timeout while opening camera")
            return False
        except Exception as e:
            print(f"Error opening camera via ADB: {e}")
            return False
    
    def capture_photo(self):
        """Capture photo based on connection type"""
        if self.connection_type in ['adb', 'adb_wifi']:
            return self.capture_photo_adb()
        elif self.connection_type == 'ip_webcam':
            return self.capture_photo_ip_webcam()
        elif self.connection_type == 'scrcpy':
            return self.capture_screenshot_scrcpy()
        return {'success': False, 'error': 'Invalid connection type'}
    
    def capture_photo_adb(self):
        """Capture a photo using Android camera via ADB"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            remote_path = f'/sdcard/DCIM/Camera/photo_{timestamp}.jpg'
            local_path = os.path.join(self.photos_dir, f'photo_{timestamp}.jpg')
            
            # Simulate camera capture by sending keyevent (camera button)
            subprocess.run([
                'adb', 'shell', 
                'input', 'keyevent', 'KEYCODE_CAMERA'
            ], check=True, timeout=5)
            
            # Wait a moment for photo to be saved
            import time
            time.sleep(2)
            
            # Get the latest photo from device
            # List files and get the most recent one
            result = subprocess.run([
                'adb', 'shell',
                'ls', '-t', '/sdcard/DCIM/Camera/*.jpg'
            ], capture_output=True, text=True, timeout=10)
            
            if result.stdout:
                latest_photo = result.stdout.strip().split('\n')[0]
                
                # Pull the photo to local machine
                subprocess.run([
                    'adb', 'pull',
                    latest_photo,
                    local_path
                ], check=True, timeout=30)
                
                return {
                    'success': True,
                    'filename': f'photo_{timestamp}.jpg',
                    'path': local_path
                }
            
            return {'success': False, 'error': 'No photo found'}
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Timeout during photo capture'}
        except Exception as e:
            print(f"Error capturing photo: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_captured_photos(self):
        """Get list of all captured photos"""
        try:
            photos = []
            for filename in os.listdir(self.photos_dir):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    photos.append({
                        'filename': filename,
                        'path': os.path.join(self.photos_dir, filename)
                    })
            return photos
        except Exception as e:
            print(f"Error getting photos: {e}")
            return []
