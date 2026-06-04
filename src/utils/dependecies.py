import subprocess
import platform
from src.utils.env_spawn import spawn

spwn = spawn()

def ensure_flathub():
    subprocess.run(
        spwn + ["flatpak", "remote-add", "--if-not-exists", "--user", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def check_OBS(): 
    arhitectura = platform.machine().lower()
    if arhitectura in ["x86_64", "amd64"]:
        result = subprocess.run(
            spwn + ["flatpak", "info", "com.obsproject.Studio"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    return False

def install_OBS():
    ensure_flathub()
    print("[SETUP] OBS is not installed, installing via Flatpak...")
    result = subprocess.run(spwn + ["flatpak", "install", "--user", "-y", "flathub", "com.obsproject.Studio"])
    return result.returncode == 0

def check():
    if not check_OBS():
        install_OBS()
        return 1
    else:
        return 1
