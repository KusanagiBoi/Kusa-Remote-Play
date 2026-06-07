import os

def spawn():
    if os.path.exists("/.flatpak-info"):
        return ["flatpak-spawn", "--host"]
    else:
        return []