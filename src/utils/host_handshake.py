import socket
import json

def host_handshake(client_ip, port=9998):
    print(f"[Handshake] Looking for client {client_ip} on port {port}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0) 
    
    sync_packet = json.dumps({"type": "sync"}).encode('utf-8')
    
    while True:
        try:
            sock.sendto(sync_packet, (client_ip, port))
            
            data, addr = sock.recvfrom(1024)
            
            if addr[0] == client_ip:
                response = json.loads(data.decode('utf-8'))
                if response.get("type") == "ack":
                    print("[Handshake] ACK received from client. Handshake successful!")
                    break
                    
        except socket.timeout:
            pass
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"[Handshake] Unexpected error: {e}")
            
    sock.close()
    return True