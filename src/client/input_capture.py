import socket
import json
import evdev
import sys
import glob
import os

def gaseste_controller_dinamic():
    print("[*] Caut controllere in /dev/input/by-id/...")
    device_uri = glob.glob('/dev/input/by-id/*-event-joystick')
    
    if not device_uri:
        return None
        
    cale_simbolica = device_uri[0]
    cale_reala = os.path.realpath(cale_simbolica)
    
    print(f"[*] Am gasit symlink: {cale_simbolica}")
    print(f"[*] Cale reala kernel: {cale_reala}")
    
    return evdev.InputDevice(cale_reala)

def verifica_conexiune_host(host_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    
    pachet_handshake = json.dumps({"type": "handshake"}).encode('utf-8')
    
    print(f"[*] Trimit handshake UDP catre {host_ip}:{port}...")
    try:
        sock.sendto(pachet_handshake, (host_ip, port))
        
        data, addr = sock.recvfrom(1024)
        raspuns = json.loads(data.decode('utf-8'))
        
        if raspuns.get("status") == "ok":
            print("[*] Handshake reusit. IP-ul este corect si host-ul asculta.")
            sock.close()
            return True
            
    except socket.timeout:
        print("[Eroare] Timeout. IP-ul e gresit sau host-ul nu asculta pe portul specificat.")
    except Exception as e:
        print(f"[Eroare] Handshake esuat: {e}")
        
    sock.close()
    return False

def start_input_capture(target_ip, target_port=9999):
    # Executam handshake-ul inainte sa ne mufam la controller
    if not verifica_conexiune_host(target_ip, target_port):
        print("[Client] Conexiunea a fost anulata din cauza erorii de IP/Handshake.")
        return

    try:
        gamepad = gaseste_controller_dinamic()
        if not gamepad:
            print("[Eroare] Nu gasesc niciun joystick conectat.")
            return
    except PermissionError:
        print("[Eroare] Permisiuni respinse pe /dev/input/. Ai uitat de sudo / reguli udev?")
        return

    print(f"[*] M-am mufat cu succes la: {gamepad.name}")
    print(f"[*] Trimit input catre {target_ip}:{target_port}...")

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
        print("\n[Client] Input capture oprit.")