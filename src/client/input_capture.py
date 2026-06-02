import socket
import json
import evdev
import sys
import glob
import os

# IP-ul de Tailscale / retea al laptopului tau
TARGET_IP = "100.104.164.55" 
TARGET_PORT = 9999

def gaseste_controller_dinamic():
    print("[*] Caut controllere in /dev/input/by-id/...")
    # Cautam orice fisier care se termina in '-event-joystick'
    device_uri = glob.glob('/dev/input/by-id/*-event-joystick')
    
    if not device_uri:
        return None
        
    # Luam primul controller gasit si rezolvam symlink-ul ca sa aflam event-ul real
    cale_simbolica = device_uri[0]
    cale_reala = os.path.realpath(cale_simbolica)
    
    print(f"[*] Am gasit symlink: {cale_simbolica}")
    print(f"[*] Cale reala kernel: {cale_reala}")
    
    return evdev.InputDevice(cale_reala)

try:
    gamepad = gaseste_controller_dinamic()
    if not gamepad:
        print("[Eroare] Nu gasesc niciun joystick conectat.")
        sys.exit(1)
except PermissionError:
    print("[Eroare] Permisiuni respinse pe /dev/input/. Ai uitat de sudo?")
    sys.exit(1)

print(f"[*] M-am mufat cu succes la: {gamepad.name}")
print(f"[*] Trimit input catre {TARGET_IP}:{TARGET_PORT}...")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    for event in gamepad.read_loop():
        if event.type != evdev.ecodes.EV_SYN:
            data = {
                "type": event.type,
                "code": event.code,
                "value": event.value
            }
            sock.sendto(json.dumps(data).encode('utf-8'), (TARGET_IP, TARGET_PORT))
except KeyboardInterrupt:
    print("\n[Client] Oprit.")