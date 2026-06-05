import socket
import json

def host_handshake(client_ip, port=9998):
    print(f"[Handshake] Looking for client {client_ip} on port {port}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0) 
    
    pachet_sync = json.dumps({"type": "sync"}).encode('utf-8')
    
    while True:
        try:
            # 1. Trimit pachetul
            sock.sendto(pachet_sync, (client_ip, port))
            
            # 2. Astept ACK (daca nu vine in 1 secunda, arunca exceptia si reia bucla)
            data, addr = sock.recvfrom(1024)
            
            # 3. Validam sursa
            if addr[0] == client_ip:
                raspuns = json.loads(data.decode('utf-8'))
                if raspuns.get("type") == "ack":
                    print("[Handshake] ACK received from client. Handshake successful!")
                    break
                    
        except socket.timeout:
            # Nu a raspuns in secunda asta, ignoram si lasam bucla sa trimita iar
            pass
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"[Handshake] Unexpected error: {e}")
            
    sock.close()
    return True