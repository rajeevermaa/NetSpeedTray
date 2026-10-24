@echo off
cd /d "%~dp0"
echo ============================================
echo   Installing NetSpeedTray - please wait...
echo ============================================

py --version >nul 2>&1
if errorlevel 1 (
  echo.
  echo Python was not found. Please install Python first from python.org
  echo and tick "Add python.exe to PATH" during install. Then run this again.
  pause
  exit /b 1
)

py -m pip install --upgrade pip
py -m pip install psutil pystray pillow pyinstaller
if errorlevel 1 (
  echo Something went wrong while downloading helpers. Check your internet.
  pause
  exit /b 1
)

echo.
echo Building the program...
py -m PyInstaller --noconsole --onefile --name NetSpeedTray netspeed.py
if not exist "dist\NetSpeedTray.exe" (
  echo Build FAILED. Take a photo of this window and send it to me.
  pause
  exit /b 1
)

taskkill /f /im NetSpeedTray.exe >nul 2>&1
mkdir "%LOCALAPPDATA%\NetSpeedTray" >nul 2>&1
copy /Y "dist\NetSpeedTray.exe" "%LOCALAPPDATA%\NetSpeedTray\NetSpeedTray.exe"

start "" "%LOCALAPPDATA%\NetSpeedTray\NetSpeedTray.exe"

echo.
echo ============================================
echo   DONE! Look at the bottom-right of your screen.
echo   It will also start by itself every time you turn on the laptop.
echo ============================================
pause
