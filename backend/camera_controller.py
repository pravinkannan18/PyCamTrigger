import subprocess
import os
from datetime import datetime

class CameraController:
    def __init__(self):
        self.photos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'captured_photos')
        os.makedirs(self.photos_dir, exist_ok=True)
        
    def check_device_connection(self):
        """Check if Android device is connected via ADB"""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            devices = result.stdout.strip().split('\n')[1:]
            connected_devices = [d for d in devices if d.strip() and 'device' in d]
            return len(connected_devices) > 0
        except Exception as e:
            print(f"Error checking device: {e}")
            return False
    
    def open_camera(self):
        """Open the camera app on Android device"""
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
            print(f"Error opening camera: {e}")
            return False
    
    def capture_photo(self):
        """Capture a photo using Android camera"""
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
