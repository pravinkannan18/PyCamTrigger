# Android Camera WebApp - Multi-Connection Support

A web application to control Android phone camera remotely using React (frontend) and Flask (backend) with **multiple connection methods**.

## 🚀 Features

- 📱 **Multiple Connection Methods**: USB, WiFi, IP Webcam, scrcpy
- 📷 Open Android camera remotely from web interface
- 📸 Capture photos remotely with a button click
- 🖼️ View captured photos in the web interface
- 💾 Save photos to local computer
- 🌐 Network-based connections (no USB required!)

## 🔌 Connection Methods

### 1. USB (ADB) - Traditional Method
- ✅ Most reliable
- ✅ Fastest transfer speeds
- ❌ Requires USB cable
- **Use case**: Direct control, best for development

### 2. WiFi (ADB)
- ✅ Wireless after initial setup
- ✅ Full ADB functionality
- ⚠️ Requires USB for initial setup
- **Use case**: Wireless control without additional apps

### 3. IP Webcam App
- ✅ No USB or ADB required
- ✅ Easy setup with Android app
- ✅ Live video streaming support
- ✅ Works over any network
- **Use case**: Easiest wireless solution, ideal for remote monitoring

### 4. scrcpy - Screen Mirroring
- ✅ Full screen mirroring
- ✅ Mouse and keyboard control
- ✅ High performance
- ⚠️ Requires ADB connection
- **Use case**: Full device control and screen capture

## 📦 Quick Start

### Backend Setup
```powershell
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```powershell
cd frontend
npm install
npm start
```

Open `http://localhost:3000` in your browser!

## 📱 Setup Instructions by Connection Method

### Method 1: USB (ADB)
1. Enable USB Debugging on Android
2. Connect via USB cable
3. Select "USB (ADB)" in web app
4. Click "Start Camera" → "Capture Photo"

### Method 2: WiFi (ADB)
1. Connect USB first and run: `adb tcpip 5555`
2. Find device IP: Settings → About → Status
3. Select "WiFi (ADB)" in web app
4. Enter IP address and connect
5. Disconnect USB cable (optional)

### Method 3: IP Webcam App
1. Install "IP Webcam" from Play Store
2. Open app and tap "Start server"
3. Note the IP address shown
4. Select "IP Webcam" in web app
5. Enter IP and port 8080

### Method 4: scrcpy
1. Install scrcpy from [GitHub](https://github.com/Genymobile/scrcpy)
2. Connect via USB or ADB WiFi
3. Select "scrcpy" in web app
4. Enjoy full screen mirroring!

## 📊 Comparison Table

| Feature | USB (ADB) | WiFi (ADB) | IP Webcam | scrcpy |
|---------|-----------|------------|-----------|--------|
| Setup | Easy | Medium | Easy | Medium |
| USB Required | Always | Initial | Never | Initial |
| Speed | Fastest | Fast | Moderate | Fast |
| Video Stream | ❌ | ❌ | ✅ | ✅ |
| Best For | Development | Wireless | Monitoring | Full Control |

## 🔧 Troubleshooting

### ADB Issues
```powershell
adb kill-server
adb start-server
adb devices
```

### IP Webcam Issues
- Ensure same WiFi network
- Check firewall settings
- Verify IP address

For detailed documentation, see the full README sections above.

## 📄 License
MIT License
