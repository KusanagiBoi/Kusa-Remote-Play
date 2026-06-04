import os
import sys
from src.utils.arm import is_obs_host_supported
from src.utils.dependecies import check
from src.utils.obs_config import force_configure_obs_stream, force_enable_obs_websocket
from src.client.video_player import receive_stream
from src.client.input_capture import start_input_capture

# Importi managerii cand ii ai gata
# from src.host.obs_manager import OBSManager
# from src.client.stream_player import run_client

def clear_screen():
    # Merge perfect pe Bazzite/Raspberry Pi
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
                
            # Restul logicii pentru HOST
            print("\n[Host] Stream Parameters:")
            target_ip = input("Client IP: ").strip()
            target_port = input("Client Port(default: 8888): ").strip()
            latency = input("Stream Latency (ms): ").strip()
            
            print(f"\n[Host] Initializing stream for {target_ip}:{target_port} with {latency} ms latency...")
            check()  # Asiguram ca OBS e instalat, daca nu, il instalam
            force_enable_obs_websocket()  # Activam WebSocket-ul (daca nu e deja)
            force_configure_obs_stream(target_ip, target_port, latency)  # Configuram OBS pentru SRT catre client
            # Aici ar trebui sa pornesti OBS-ul folosind
            # setup_obs_environment(target_ip, target_port, latency)
            # manager = OBSManager()
            # manager.start_obs_process()
            # ... samd

            input("\nPress ENTER to return to menu...")
            
        elif option == '2':
            print("\n[Client] Connection Parameters:")
            host_ip = input("HOST IP: ").strip()
            
            print(f"\n[Client] Connecting to {host_ip}...")
            receive_stream()
            start_input_capture(host_ip)
            input("\nPress ENTER to return to menu...")
            
        elif option == '0':
            print("\nClosing application. Goodbye!")
            sys.exit(0)
            
        else:
            print("\n[!] Invalid option. Please try again.")
            input("Press ENTER to return to menu...")

if __name__ == "__main__":
    run_menu()