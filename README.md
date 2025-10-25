# Android Camera WebApp

A web application to control Android phone camera remotely using React (frontend) and Flask (backend).

## Features

- 📱 Connect to Android device via USB
- 📷 Open Android camera remotely from web interface
- 📸 Capture photos remotely with a button click
- 🖼️ View captured photos in the web interface
- 💾 Save photos to local computer

## Project Structure

```
android-camera-webapp/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── camera_controller.py   # Android camera control logic
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styles
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env
└── captured_photos/           # Saved photos from camera
```

## Prerequisites

1. **ADB (Android Debug Bridge)** - Install ADB on your computer
   - Windows: Download from [Android Developer site](https://developer.android.com/tools/releases/platform-tools)
   - Mac: `brew install android-platform-tools`
   - Linux: `sudo apt-get install adb`

2. **Android Device Setup**
   - Enable Developer Options (Settings > About Phone > Tap Build Number 7 times)
   - Enable USB Debugging (Settings > Developer Options > USB Debugging)
   - Connect device via USB cable

3. **Python 3.8+** installed
4. **Node.js 14+** and npm installed

## Installation

### Backend Setup

1. Navigate to backend directory:
   ```powershell
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```powershell
   cd frontend
   ```

2. Install npm dependencies:
   ```powershell
   npm install
   ```

## Running the Application

### 1. Start the Backend Server

```powershell
cd backend
python app.py
```

The Flask server will start on `http://localhost:5000`

### 2. Start the Frontend Development Server

In a new terminal:

```powershell
cd frontend
npm start
```

The React app will start on `http://localhost:3000`

### 3. Connect Your Android Device

1. Connect your Android phone via USB
2. Make sure USB debugging is enabled
3. Accept the USB debugging prompt on your phone
4. Verify connection by running: `adb devices`

## Usage

1. Open your browser to `http://localhost:3000`
2. Check if your device is connected (green status indicator)
3. Click **"Start Camera"** button to open the camera app on your phone
4. Click **"Capture Photo"** button to take a picture
5. The captured photo will be displayed in the web interface
6. Photos are saved in the `captured_photos/` directory

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/check-device` - Check if Android device is connected
- `POST /api/open-camera` - Open camera app on Android device
- `POST /api/capture-photo` - Capture a photo
- `GET /api/photos` - Get list of captured photos
- `GET /api/photos/<filename>` - Get a specific photo

## Troubleshooting

### Device Not Detected
- Make sure USB debugging is enabled
- Try different USB cable or port
- Run `adb devices` in terminal to verify connection
- Revoke USB debugging authorizations and reconnect

### Camera Won't Open
- Grant camera permissions on your phone
- Make sure no other app is using the camera
- Restart ADB: `adb kill-server` then `adb start-server`

### Backend Connection Error
- Verify Flask server is running on port 5000
- Check firewall settings
- Ensure CORS is properly configured

## Technologies Used

- **Frontend**: React.js, Axios, CSS3
- **Backend**: Flask, Flask-CORS
- **Device Control**: ADB (Android Debug Bridge)
- **Communication**: REST API

## License

MIT License

## Notes

- This application requires a physical connection via USB
- Make sure your Android device has sufficient permissions
- Photos are captured using ADB commands and transferred to your computer
