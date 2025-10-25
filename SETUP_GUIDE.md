# 📱 Android Camera WebApp - Complete Setup Guide

**Step-by-step instructions to get your Android camera controller up and running!**

---

## 📋 Table of Contents
1. [Prerequisites Installation](#step-1-prerequisites-installation)
2. [Project Setup](#step-2-project-setup)
3. [Android Device Preparation](#step-3-android-device-preparation)
4. [Choose Your Connection Method](#step-4-choose-your-connection-method)
5. [Running the Application](#step-5-running-the-application)
6. [First Use & Testing](#step-6-first-use--testing)
7. [Troubleshooting](#step-7-troubleshooting)

---

## Step 1: Prerequisites Installation

### 1.1 Install Python (if not installed)

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.8 or higher
3. Run installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"
6. Verify installation:
   ```powershell
   python --version
   ```
   Should show: `Python 3.x.x`

**Mac:**
```bash
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### 1.2 Install Node.js and npm

**Windows:**
1. Go to [nodejs.org](https://nodejs.org/)
2. Download LTS version (recommended)
3. Run installer
4. Click "Next" through all steps
5. Verify installation:
   ```powershell
   node --version
   npm --version
   ```

**Mac:**
```bash
brew install node
node --version
npm --version
```

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
```

### 1.3 Install ADB (Android Debug Bridge)

**Choose ONE connection method below:**

#### Option A: USB Connection (Required for all methods)

**Windows:**
1. Download [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools)
2. Extract ZIP file to `C:\platform-tools\`
3. Add to PATH:
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System Variables", find "Path"
   - Click "Edit" → "New"
   - Add: `C:\platform-tools`
   - Click "OK" on all dialogs
4. Open NEW PowerShell window and verify:
   ```powershell
   adb --version
   ```

**Mac:**
```bash
brew install android-platform-tools
adb --version
```

**Linux:**
```bash
sudo apt update
sudo apt install adb
adb --version
```

#### Option B: IP Webcam App (No ADB needed!)

1. Skip ADB installation
2. Install "IP Webcam" app from Google Play Store
3. Ensure phone and computer are on same WiFi network

#### Option C: scrcpy (Optional - for screen mirroring)

**Windows:**
```powershell
# Using Scoop package manager
scoop install scrcpy

# OR download from GitHub
# https://github.com/Genymobile/scrcpy/releases
```

**Mac:**
```bash
brew install scrcpy
```

**Linux:**
```bash
sudo snap install scrcpy
```

---

## Step 2: Project Setup

### 2.1 Download/Clone the Project

**If using Git:**
```powershell
cd P:\My_Project
git clone <your-repo-url>
cd android-camera-webapp
```

**If downloaded as ZIP:**
1. Extract ZIP file to `P:\My_Project\android-camera-webapp`
2. Open PowerShell in that folder

### 2.2 Project Structure Verification

Verify you have this structure:
```
android-camera-webapp/
├── backend/
│   ├── app.py
│   ├── camera_controller.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
├── captured_photos/
└── README.md
```

### 2.3 Backend Setup

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# For PowerShell:
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# For Command Prompt:
# venv\Scripts\activate.bat

# Install Python dependencies
pip install -r requirements.txt

# You should see installation of:
# - Flask
# - Flask-CORS
# - requests
```

**Expected Output:**
```
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 requests-2.31.0 ...
```

### 2.4 Frontend Setup

Open a **NEW** PowerShell window:

```powershell
# Navigate to frontend folder
cd P:\My_Project\android-camera-webapp\frontend

# Install npm dependencies
npm install

# This will take 2-5 minutes
# You should see installation of:
# - react
# - react-dom
# - axios
# - react-scripts
```

**Expected Output:**
```
added 1500+ packages in 2m
```

---

## Step 3: Android Device Preparation

### 3.1 Enable Developer Options

1. Open **Settings** on your Android phone
2. Scroll to **About Phone** (or **About Device**)
3. Find **Build Number**
4. **Tap "Build Number" 7 times**
5. You'll see: "You are now a developer!"

### 3.2 Enable USB Debugging (For USB/WiFi ADB)

1. Go back to **Settings**
2. Find **Developer Options** (usually under System)
3. Enable **USB Debugging**
4. Enable **Stay Awake** (optional but recommended)

### 3.3 Grant Necessary Permissions

When you connect:
1. You'll see "Allow USB debugging?" popup
2. Check "Always allow from this computer"
3. Tap **OK**

---

## Step 4: Choose Your Connection Method

### Method A: USB Connection (Easiest to Start)

**Step-by-step:**

1. **Connect Phone via USB Cable**
   - Use a data-capable USB cable (not charge-only)
   - Connect phone to computer

2. **Verify Connection**
   ```powershell
   adb devices
   ```
   
   **Expected Output:**
   ```
   List of devices attached
   ABC123XYZ    device
   ```
   
   ✅ If you see your device ID and "device" → SUCCESS!
   
   ❌ If you see "unauthorized" → Check phone for authorization popup
   
   ❌ If empty list → Try different cable or USB port

3. **Test ADB**
   ```powershell
   adb shell echo "Connected!"
   ```
   Should print: `Connected!`

---

### Method B: WiFi (ADB) - Wireless Connection

**Prerequisites:** USB connection working first

**Step-by-step:**

1. **Connect via USB first** (see Method A)

2. **Enable TCP/IP mode**
   ```powershell
   adb tcpip 5555
   ```
   Output: `restarting in TCP mode port: 5555`

3. **Find Your Phone's IP Address**
   
   **Option 1 - Via ADB:**
   ```powershell
   adb shell ip addr show wlan0 | findstr "inet "
   ```
   
   **Option 2 - On Phone:**
   - Settings → About Phone → Status → IP Address
   - OR Settings → WiFi → Connected Network → IP Address
   
   Example IP: `192.168.1.100`

4. **Connect via WiFi**
   ```powershell
   adb connect 192.168.1.100:5555
   ```
   Output: `connected to 192.168.1.100:5555`

5. **Verify Connection**
   ```powershell
   adb devices
   ```
   Should show: `192.168.1.100:5555    device`

6. **Disconnect USB Cable** (optional)
   - Your phone is now connected wirelessly!

**To reconnect later:**
```powershell
adb connect 192.168.1.100:5555
```

**To return to USB mode:**
```powershell
adb usb
```

---

### Method C: IP Webcam App - Easiest Wireless

**No USB or ADB required!**

**Step-by-step:**

1. **Install IP Webcam App**
   - Open Google Play Store on your Android
   - Search: "IP Webcam"
   - Install app by **Pavel Khlebovich**
   - Open the app

2. **Configure App (Optional)**
   - Scroll through settings
   - Video Resolution: Choose quality (720p recommended)
   - Photo Resolution: Maximum quality
   - Enable features you want

3. **Start Server**
   - Scroll to bottom of app
   - Tap **"Start server"**
   - App will show: `Running on: http://192.168.1.100:8080`
   - **Note this IP address!**

4. **Verify Server is Running**
   - Open browser on computer
   - Go to: `http://192.168.1.100:8080`
   - You should see IP Webcam control page
   - You can see live video feed!

5. **Keep App Running**
   - Don't close the app
   - Keep phone screen on (or enable "Prevent phone sleeping")

**Network Requirements:**
- ✅ Phone and computer on SAME WiFi network
- ✅ OR computer can access phone's IP
- ❌ Won't work if devices on different networks

---

### Method D: scrcpy - Screen Mirroring

**Prerequisites:** ADB connection working (USB or WiFi)

**Step-by-step:**

1. **Install scrcpy** (see Step 1.3C)

2. **Connect Device** (USB or WiFi ADB)
   ```powershell
   adb devices
   ```

3. **Test scrcpy**
   ```powershell
   scrcpy
   ```
   
   ✅ Should open window showing phone screen
   
   ❌ If error, ensure device is authorized

4. **Close scrcpy** (for now)
   - Press Ctrl+C in terminal
   - Or close the window

5. **Ready to use with web app!**

---

## Step 5: Running the Application

### 5.1 Start Backend Server

**Terminal 1 (PowerShell):**

```powershell
# Navigate to backend
cd P:\My_Project\android-camera-webapp\backend

# Activate virtual environment (if using)
.\venv\Scripts\Activate.ps1

# Start Flask server
python app.py
```

**Expected Output:**
```
Starting Flask server...
Make sure:
1. Android device is connected via USB
2. USB debugging is enabled
3. ADB is installed and in PATH
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

✅ **Leave this terminal running!**

### 5.2 Start Frontend Server

**Terminal 2 (NEW PowerShell window):**

```powershell
# Navigate to frontend
cd P:\My_Project\android-camera-webapp\frontend

# Start React development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view android-camera-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.50:3000

webpack compiled with 0 warnings
```

✅ **Browser should open automatically!**

If not, manually open: `http://localhost:3000`

---

## Step 6: First Use & Testing

### 6.1 Web Interface Overview

When you open `http://localhost:3000`, you'll see:

```
╔════════════════════════════════════════════╗
║     📱 Android Camera Controller          ║
╠════════════════════════════════════════════╣
║ Connection Method: [Dropdown ▼]           ║
║  ● Device Connected / ○ Device Not Conn   ║
║  [🔄 Refresh Connection]                  ║
╠════════════════════════════════════════════╣
║  [📷 Start Camera]                        ║
║  [📸 Capture Photo]                       ║
╠════════════════════════════════════════════╣
║  Latest Capture: [Photo Preview]          ║
╠════════════════════════════════════════════╣
║  📋 Connection Methods (Instructions)      ║
╚════════════════════════════════════════════╝
```

### 6.2 Test USB/ADB Connection

1. **Select Connection Method**
   - Dropdown: **"USB (ADB)"**

2. **Check Status**
   - Look for green dot: ● **Device Connected**
   - If red, click **"Refresh Connection"**

3. **Open Camera**
   - Click **"📷 Start Camera"**
   - Your phone's camera app should open!
   - ✅ Success message appears

4. **Capture Photo**
   - Click **"📸 Capture Photo"**
   - Wait 2-3 seconds
   - Photo appears in web interface!
   - Photo saved to: `captured_photos/` folder

### 6.3 Test WiFi Connection

1. **Select Connection Method**
   - Dropdown: **"WiFi (ADB)"**

2. **Connection Dialog Opens**
   - Enter IP Address: `192.168.1.100`
   - Port: `5555`
   - Click **"Connect"**

3. **Wait for connection**
   - Success: Green status, "Connected to..."
   - Failure: Try IP address again

4. **Test Camera** (same as USB)

### 6.4 Test IP Webcam

1. **Start IP Webcam app on phone** (see Step 4C)

2. **Select Connection Method**
   - Dropdown: **"IP Webcam"**

3. **Connection Dialog Opens**
   - Enter IP Address: `192.168.1.100`
   - Port: `8080`
   - Click **"Connect"**

4. **No need to "Start Camera"!**
   - IP Webcam IS the camera
   - Just click **"📸 Capture Photo"**
   - Photo captured instantly!

### 6.5 Test scrcpy

1. **Select Connection Method**
   - Dropdown: **"scrcpy"**

2. **Device must be connected** (USB or WiFi ADB)

3. **Optional: Start scrcpy manually**
   ```powershell
   scrcpy
   ```
   - See phone screen on computer!

4. **Capture Screenshot**
   - Click **"📸 Capture Photo"**
   - Takes screenshot of current screen

---

## Step 7: Troubleshooting

### Problem: "Device Not Connected"

**For USB:**
```powershell
# Check device is connected
adb devices

# If empty:
# 1. Try different USB cable
# 2. Try different USB port
# 3. Check phone for authorization popup
# 4. Restart ADB:
adb kill-server
adb start-server
adb devices
```

**For WiFi:**
```powershell
# Reconnect
adb connect <IP>:5555

# If fails:
# 1. Verify IP address is correct
# 2. Ensure same WiFi network
# 3. Restart from USB setup
```

**For IP Webcam:**
- Check IP address in app
- Try opening `http://<IP>:8080` in browser
- Ensure same WiFi network
- Restart server in app

### Problem: "Backend Connection Error"

**Check Backend is Running:**
```powershell
# In Terminal 1, you should see:
Running on http://127.0.0.1:5000
```

**If not running:**
```powershell
cd backend
python app.py
```

**Test Backend Directly:**
```powershell
curl http://localhost:5000/api/health
```
Should return: `{"status":"ok"}`

### Problem: Frontend Won't Start

**Common Causes:**

1. **Port 3000 already in use:**
   ```powershell
   # Kill process on port 3000
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   
   # Or choose different port
   $env:PORT=3001; npm start
   ```

2. **Missing dependencies:**
   ```powershell
   cd frontend
   rm -r node_modules
   rm package-lock.json
   npm install
   npm start
   ```

### Problem: "Camera won't open"

**Solutions:**
1. Grant camera permissions on phone
2. Close any other app using camera
3. Restart phone
4. Try manual command:
   ```powershell
   adb shell am start -a android.media.action.IMAGE_CAPTURE
   ```

### Problem: "Photo capture fails"

**Solutions:**
1. Open camera manually on phone first
2. Take one photo manually
3. Grant storage permissions
4. Check available storage space
5. Try screenshot instead:
   ```powershell
   adb shell screencap -p /sdcard/test.png
   adb pull /sdcard/test.png
   ```

### Problem: "Cannot find Python/Node"

**Add to PATH manually:**

**Windows:**
1. Win + X → System → Advanced system settings
2. Environment Variables → Path → Edit
3. Add Python path: `C:\Users\<User>\AppData\Local\Programs\Python\Python3x\`
4. Add npm path: `C:\Program Files\nodejs\`
5. Restart PowerShell

### Problem: "ADB not found"

```powershell
# Windows - Install via Chocolatey
choco install adb

# Or add to PATH:
# C:\platform-tools

# Verify
adb --version
```

### Problem: "Execution Policy Error"

```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

# Or for current user only:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: "Permission Denied on Linux/Mac"

```bash
# Give permissions to ADB
sudo chmod +x adb

# Or run with sudo
sudo adb devices

# Fix udev rules (Linux)
sudo usermod -aG plugdev $USER
```

---

## 🎉 Success Checklist

After completing setup, you should be able to:

- ✅ Backend server running on port 5000
- ✅ Frontend running on port 3000
- ✅ Device shows as "Connected" (green dot)
- ✅ Can click "Start Camera" → Camera opens
- ✅ Can click "Capture Photo" → Photo appears
- ✅ Photos saved in `captured_photos/` folder
- ✅ Can switch between connection methods

---

## 📞 Need More Help?

### Useful Commands

**Check everything is working:**
```powershell
# Python version
python --version

# Node version
node --version
npm --version

# ADB version
adb --version

# Check device
adb devices

# Check backend
curl http://localhost:5000/api/health

# Check frontend
curl http://localhost:3000
```

### Logs to Check

**Backend logs:** Terminal 1 (where you ran `python app.py`)
**Frontend logs:** Terminal 2 (where you ran `npm start`)
**Browser console:** F12 → Console tab

---

## 🚀 Next Steps

Once everything is working:

1. **Bookmark** `http://localhost:3000`
2. **Try different connection methods**
3. **Take multiple photos**
4. **Check `captured_photos/` folder**
5. **Experiment with scrcpy screen mirroring**
6. **Try IP Webcam video streaming**

---

**Happy Camera Controlling! 📸**
