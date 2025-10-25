# Quick ADB Installation Guide for Windows

## ✅ Method 1: Download Android Platform Tools (RECOMMENDED - Easiest)

### Step 1: Download
1. Open this link in your browser:
   👉 **https://developer.android.com/tools/releases/platform-tools**

2. Click **"Download SDK Platform-Tools for Windows"**
   - File: `platform-tools-latest-windows.zip` (about 10-15 MB)

### Step 2: Extract
1. Go to your Downloads folder
2. Right-click `platform-tools-latest-windows.zip`
3. Choose **"Extract All..."**
4. Extract to: `C:\platform-tools\`
   - Or any location you prefer (e.g., `C:\Users\YourName\platform-tools\`)

### Step 3: Add to PATH
1. Press **Win + X** → Click **"System"**
2. Click **"Advanced system settings"** (on the right side)
3. Click **"Environment Variables"** button
4. Under **"System variables"** (bottom section), find **"Path"**
5. Select **"Path"** → Click **"Edit"**
6. Click **"New"**
7. Type: `C:\platform-tools`
8. Click **"OK"** on all dialogs

### Step 4: Verify Installation
**IMPORTANT:** Open a **NEW** PowerShell window (close old ones)

```powershell
adb --version
```

Expected output:
```
Android Debug Bridge version 1.x.x
...
```

---

## ⚡ Method 2: Using Chocolatey (If you have Chocolatey installed)

```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install ADB
choco install adb
```

---

## ⚡ Method 3: Using Scoop (If you have Scoop installed)

```powershell
# Install Scoop first (if not installed)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Then install ADB
scoop install adb
```

---

## 🎯 QUICK START (For those who want to skip ADB)

### Use IP Webcam Instead - NO ADB NEEDED!

If you want to start immediately without ADB:

1. **On Your Android Phone:**
   - Open **Google Play Store**
   - Search: **"IP Webcam"**
   - Install app by **Pavel Khlebovich**
   - Open the app
   - Scroll to bottom
   - Tap **"Start server"**
   - Note the IP address shown (e.g., `http://192.168.1.100:8080`)

2. **Run the WebApp:**
   ```powershell
   # Terminal 1: Backend
   cd backend
   pip install -r requirements.txt
   python app.py

   # Terminal 2: Frontend
   cd frontend
   npm install
   npm start
   ```

3. **In the Web Interface:**
   - Select **"IP Webcam"** from dropdown
   - Enter your phone's IP address
   - Click **"Connect"**
   - Click **"📸 Capture Photo"**
   - Done! No USB, no ADB needed!

---

## 🔧 Troubleshooting

### After installing ADB, still not found?

**1. Restart PowerShell**
- Close ALL PowerShell windows
- Open a NEW PowerShell window

**2. Check PATH manually**
```powershell
$env:Path -split ';' | Select-String "platform-tools"
```

**3. Add to PATH temporarily (for current session only)**
```powershell
$env:Path += ";C:\platform-tools"
adb --version
```

**4. Verify ADB file exists**
```powershell
Test-Path "C:\platform-tools\adb.exe"
# Should return: True
```

---

## 📝 Which Method Should I Choose?

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Manual Download** | ✅ No extra tools<br>✅ Official source<br>✅ Always works | ⏰ Manual PATH setup | Most users |
| **Chocolatey** | ✅ Automatic<br>✅ Easy updates | ❌ Requires Chocolatey | Developers |
| **Scoop** | ✅ Automatic<br>✅ Clean installs | ❌ Requires Scoop | Power users |
| **IP Webcam** | ✅ No ADB needed!<br>✅ Works immediately | ⚠️ Network required | Quick start |

---

## ✅ Next Steps After Installing ADB

1. **Close and reopen PowerShell**
2. **Verify ADB works:**
   ```powershell
   adb --version
   adb devices
   ```

3. **Connect your Android device:**
   - Enable USB Debugging (see SETUP_GUIDE.md Step 3)
   - Connect via USB
   - Run: `adb devices`
   - You should see your device listed!

4. **Continue with the main setup:**
   - Follow SETUP_GUIDE.md from Step 2 onwards

---

**Need help? Check SETUP_GUIDE.md for complete instructions!**
