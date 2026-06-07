import socket
import json

def client_handshake(host_ip, port=9998):
    print(f"[Handshake] Looking for host {host_ip} on port {port}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    
    ack_packet = json.dumps({"type": "ack"}).encode('utf-8')
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            
            if addr[0] == host_ip:
                message = json.loads(data.decode('utf-8'))
                
                if message.get("type") == "sync":
                    print(f"[Handshake] Sync packet received from {host_ip}. Sending ACK.")
                    sock.sendto(ack_packet, addr)
                    break 
                    
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"[Handshake] Unexpected error: {e}")
            
    sock.close()
    return True