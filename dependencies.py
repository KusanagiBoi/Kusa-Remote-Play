import subprocess
from spawn import spawn

spwn = spawn()
subprocess.run(spwn + ["flatpak", "remote-add", "--if-not-exists", "--user", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"])

def check_OBS(): #Checks if the system has OBS installed as a Flatpak
    result = subprocess.run(
        ["flatpak", "info", "com.obsproject.Studio"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def check_MPV(): #Checks if the system has MPV installed as a Flatpak
    result = subprocess.run(
        ["flatpak", "info", "io.mpv.Mpv"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def check_Dependencies():
    if not check_OBS(): 
        subprocess.run(spwn + ["flatpak", "install", "--user", "-y", "flathub", "com.obsproject.Studio"]) #installs the OBS flatpak

    if not check_MPV():
        subprocess.run(spwn + ["flatpak", "install", "--user", "-y", "flathub", "io.mpv.Mpv"]) #installs the MPV flatpak
    
    if check_OBS() and check_MPV():
        return 1
    else:
        print("At least one dependecy could not be installed")



check_Dependencies() 