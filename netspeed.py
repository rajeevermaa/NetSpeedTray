"""
NetSpeedTray - shows live download/upload speed as a system tray icon.
The icon redraws itself every second. Hover for full details.
Right-click: toggle "Start with Windows" or Exit.
"""
import os
import sys
import time
import winreg

import psutil
import pystray
from PIL import Image, ImageDraw, ImageFont

APP_NAME = "NetSpeedTray"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), APP_NAME)
MARKER = os.path.join(DATA_DIR, ".configured")

running = True


# ---------- start with Windows ----------
def startup_command():
    if getattr(sys, "frozen", False):          # running as the built .exe
        return f'"{sys.executable}"'
    pyw = sys.executable.replace("python.exe", "pythonw.exe")
    return f'"{pyw}" "{os.path.abspath(__file__)}"'


def is_startup_enabled():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ) as k:
            winreg.QueryValueEx(k, APP_NAME)
            return True
    except OSError:
        return False


def set_startup(enable):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as k:
            if enable:
                winreg.SetValueEx(k, APP_NAME, 0, winreg.REG_SZ, startup_command())
            else:
                try:
                    winreg.DeleteValue(k, APP_NAME)
                except FileNotFoundError:
                    pass
    except OSError:
        pass


def first_run_setup():
    """Turn on 'start with Windows' only the very first time."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(MARKER):
        set_startup(True)
        open(MARKER, "w").close()


# ---------- formatting ----------
def short(bps):
    """Return (number_text, unit_text) for the icon. bps = bits per second."""
    kbps = bps / 1000
    if kbps < 1000:
        return f"{kbps:.0f}", "kbps"
    mbps = kbps / 1000
    if mbps < 1000:
        return (f"{mbps:.1f}" if mbps < 10 else f"{mbps:.0f}"), "Mbps"
    return f"{mbps / 1000:.1f}", "Gbps"


def full(bps):
    num, unit = short(bps)
    return f"{num} {unit}"


# ---------- icon drawing ----------
def load_font(size):
    for name in ("arialbd.ttf", "segoeuib.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fit_text(draw, text, max_w, start_size):
    size = start_size
    while size > 8:
        font = load_font(size)
        box = draw.textbbox((0, 0), text, font=font)
        if box[2] - box[0] <= max_w:
            return font, box
        size -= 2
    font = load_font(8)
    return font, draw.textbbox((0, 0), text, font=font)


def text_color():
    """White text on dark taskbar, black text on light taskbar."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as k:
            light = winreg.QueryValueEx(k, "SystemUsesLightTheme")[0]
        return (0, 0, 0, 255) if light else (255, 255, 255, 255)
    except OSError:
        return (255, 255, 255, 255)


def make_icon(down_bps):
    S = 64
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))   # transparent background
    d = ImageDraw.Draw(img)
    num, unit = short(down_bps)
    col = text_color()

    font, box = fit_text(d, num, S, 52)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text(((S - w) / 2 - box[0], (34 - h) / 2 - box[1]), num, font=font, fill=col)

    font2, box2 = fit_text(d, unit, S, 34)
    w2, h2 = box2[2] - box2[0], box2[3] - box2[1]
    d.text(((S - w2) / 2 - box2[0], 34 + (30 - h2) / 2 - box2[1]), unit, font=font2, fill=col)
    return img


# ---------- measuring ----------
def read_counters():
    sent = recv = 0
    for name, c in psutil.net_io_counters(pernic=True).items():
        if "loopback" in name.lower():
            continue
        sent += c.bytes_sent
        recv += c.bytes_recv
    return sent, recv


def worker(icon):
    icon.visible = True
    last_sent, last_recv = read_counters()
    last_t = time.time()
    while running:
        time.sleep(1)
        sent, recv = read_counters()
        now = time.time()
        dt = max(now - last_t, 0.001)
        down = max(recv - last_recv, 0) * 8 / dt
        up = max(sent - last_sent, 0) * 8 / dt
        last_sent, last_recv, last_t = sent, recv, now
        try:
            icon.icon = make_icon(down)
            icon.title = f"Download: {full(down)}\nUpload: {full(up)}"
        except Exception:
            pass


# ---------- menu ----------
def toggle_startup(icon, item):
    set_startup(not is_startup_enabled())


def quit_app(icon, item):
    global running
    running = False
    icon.stop()


def main():
    first_run_setup()
    menu = pystray.Menu(
        pystray.MenuItem("Start with Windows", toggle_startup,
                         checked=lambda item: is_startup_enabled()),
        pystray.MenuItem("Exit", quit_app),
    )
    icon = pystray.Icon(APP_NAME, make_icon(0), "Starting...", menu)
    icon.run(setup=worker)


if __name__ == "__main__":
    main()
