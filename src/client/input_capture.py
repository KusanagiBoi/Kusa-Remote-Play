import socket
import json
import evdev
import sys
import glob
import os

def find_gamepads():
    print("[*] Searching gamepads in /dev/input/by-id/...")
    devices = glob.glob('/dev/input/by-id/*-event-joystick')
    
    if not devices:
        return None
        
    symlink = devices[0]
    path = os.path.realpath(symlink)
    
    print(f"[*] symlink: {symlink}")
    print(f"[*] Real path: {path}")
    
    return evdev.InputDevice(path)

def start_input_capture(target_ip, target_port=9999):

    try:
        gamepad = find_gamepads()
        if not gamepad:
            print("[Error] No pads connected. Please connect a gamepad and try again.")
            return
    except PermissionError:
        print("[Error] Permission denied when trying to access the gamepad. Please run the script with appropriate permissions (e.g., using sudo) or adjust device permissions.")
        return

    print(f"[*] Found gamepad: {gamepad.name}")
    print(f"[*] Sending input to {target_ip}:{target_port}...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        for event in gamepad.read_loop():
            if event.type != evdev.ecodes.EV_SYN:
                data = {
                    "type": event.type,
                    "code": event.code,
                    "value": event.value
                }
                sock.sendto(json.dumps(data).encode('utf-8'), (target_ip, target_port))
    except KeyboardInterrupt:
        print("\n[Client] Input capture stopped.")