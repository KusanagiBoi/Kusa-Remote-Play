'''Automatically detects if the python script is ran in a flatpak sandbox or not'''
import os

def spawn():
    if os.path.exists("/.flatpak-info"): 
        return ["flatpak-spawn", "--host"]
    else:
        return []
