# NetSpeedTray

**Live internet speed in your Windows 11 taskbar, just like the speed indicator on Android phones.**

Simple. Minimal. No windows, no clutter. A small number next to your clock showing how fast your internet is moving right now.

<!-- Add a screenshot: upload an image to the repo and replace the line below -->
<!-- ![Screenshot](screenshot.png) -->

## Features
- Live download speed shown in the system tray (updates every second)
- Auto units: **kbps**, **Mbps**, **Gbps**
- Hover to see both download and upload speed
- Text color adapts to light or dark taskbar
- Starts automatically with Windows
- Lightweight, free, no ads, no tracking, works offline (only reads your own network counters)

## Install (easy way, no coding knowledge needed)
1. Install **Python** from [python.org/downloads](https://www.python.org/downloads/). During setup, tick **"Add python.exe to PATH"**.
2. Click the green **Code** button on this page, then **Download ZIP**, and unzip it.
3. Double-click **`install.bat`** and wait for **DONE!** (needs internet, takes 1-3 minutes).
4. Look at the bottom-right of your screen. If you don't see the number, click the **^** arrow and drag the icon next to your Wi-Fi icon.

If Windows says "Windows protected your PC", click **More info → Run anyway**. The full code is in this repo for you to read.

## Usage
- **Hover** the icon: see download and upload speed.
- **Right-click**: turn "Start with Windows" on/off, or Exit.

## Uninstall
1. Right-click the icon → untick **Start with Windows** → **Exit**.
2. Delete the folder `%LOCALAPPDATA%\NetSpeedTray`.

## Notes
- This shows your **current** network activity, not a speed test. It reads close to 0 when nothing is using the internet.
- Counts all network adapters except loopback (Wi-Fi + Ethernet combined).
- Windows does not allow plain text in the taskbar, so the app redraws a tray icon every second.

## Built with
Python, [psutil](https://github.com/giampaolo/psutil), [pystray](https://github.com/moses-palmer/pystray), [Pillow](https://python-pillow.org/), PyInstaller.

## About
Created with AI assistance by a non-programmer who wanted a simple speed indicator on Windows like the one on Samsung phones. Contributions and suggestions are welcome via Issues.

## License
MIT, see [LICENSE](LICENSE).
