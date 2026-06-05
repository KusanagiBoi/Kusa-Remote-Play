import os
import sys
import threading
from src.utils.arm import is_obs_host_supported
from src.utils.dependecies import check
from src.utils.obs_config import force_configure_obs_stream, force_enable_obs_websocket
from src.client.video_player import receive_stream
from src.client.input_capture import start_input_capture
from src.utils.host_handshake import host_handshake
from src.utils.client_handshake import client_handshake
from src.host.obs_manager import OBSManager
from src.host.input_emulator import InputReceiver

def clear_screen():
    os.system('clear')

def show_menu():
    clear_screen()
    print("====================================")
    print("       KUSA REMOTE PLAY v1.0        ")
    print("====================================")
    print("1. HOST")
    print("2. JOIN")
    print("0. QUIT")
    print("====================================")

def run_menu():
    host_supported = is_obs_host_supported()
    
    while True:
        show_menu()
        option = input("Select an option: ").strip()
        
        if option == '1':
            if not host_supported:
                print("\n[!] Error: Hosting is not available on this architecture.")
                input("Press ENTER to return to menu...")
                continue
                
            print("\n[Host] Stream Parameters:")
            target_ip = input("Client IP: ").strip()
            target_port = input("Client Port (default: 8888): ").strip()
            latency = input("Stream Latency (ms): ").strip()
            
            # Fallback automat daca dai doar ENTER la port
            if not target_port:
                target_port = "8888"
                
            print(f"\n[Host] Initializing stream for {target_ip}:{target_port} with {latency} ms latency...")
            check()  
            host_handshake(target_ip)  
            force_enable_obs_websocket()  
            force_configure_obs_stream(target_ip, target_port, latency)  
            
            obs = OBSManager()
            receptor = InputReceiver() 
            
            obs.launch_obs()
            obs.connect()
            obs.setup_display_capture()
            obs.start_stream()
            
            print("\n[Host] Stream activ. Astept input de la client. (Apasa Ctrl+C pentru oprire)")
            
            # Executia se blocheaza aici pe thread-ul principal
            receptor.start() 
            
            # Dupa ce dai Ctrl+C pe Host, iese din receptor.start() si ajunge aici
            print("\n[Host] Opresc stream-ul...")
            obs.stop_stream()
            obs.disconnect()   

            input("\nPress ENTER to return to menu...")
            
        elif option == '2':
            print("\n[Client] Connection Parameters:")
            host_ip = input("HOST IP: ").strip()
            
            if not host_ip:
                print("[!] Eroare: Nu ai introdus un IP.")
                input("Press ENTER to return to menu...")
                continue
                
            print(f"\n[Client] Connecting to {host_ip}...")
            client_handshake(host_ip)
            
            print("[Client] Pornesc stream-ul video in fundal...")
            # Thread separat pentru video ca sa nu blocheze terminalul
            video_thread = threading.Thread(target=receive_stream)
            video_thread.daemon = True 
            video_thread.start()
            
            print("[Client] Preluare input activa. (Apasa Ctrl+C pentru oprire)")
            # Preluarea de input ramane pe firul principal ca sa o poti opri la tastatura
            start_input_capture(host_ip)
            
            input("\nPress ENTER to return to menu...")
            
        elif option == '0':
            print("\nClosing application. Goodbye!")
            sys.exit(0)
            
        else:
            print("\n[!] Invalid option. Please try again.")
            input("Press ENTER to return to menu...")