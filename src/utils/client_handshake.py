import socket
import json

def client_handshake(host_ip, port=9998):
    print(f"[Handshake] Looking for host {host_ip} on port {port}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    
    pachet_ack = json.dumps({"type": "ack"}).encode('utf-8')
    
    while True:
        try:
            # Blocheaza executia la infinit pana primeste ceva
            data, addr = sock.recvfrom(1024)
            
            # Filtram pachetele de zgomot, acceptam STRICT de la host_ip
            if addr[0] == host_ip:
                mesaj = json.loads(data.decode('utf-8'))
                
                if mesaj.get("type") == "sync":
                    print(f"[Handshake] Sync packet received from {host_ip}. Sending ACK.")
                    sock.sendto(pachet_ack, addr)
                    break # Iesim din bucla, drumul e liber
                    
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"[Handshake] Unexpected error: {e}")
            
    sock.close()
    return True