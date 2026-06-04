import os
import sys


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
    while True:
        show_menu()
        option = input("Select an option: ").strip()
        
        if option == '1':
            print("\n[Host] Stream Parameters:")
            target_ip = input("Client IP: ").strip()
            target_port = input("Client Port(default: 8888): ").strip()
            latency = input("Stream Latency (ms): ").strip()
            
            print(f"\n[Host] Initializing stream for {target_ip}:{target_port} with {latency} ms latency...")
            # Aici apelezi:
            # setup_obs_environment(target_ip, target_port, latency)
            # manager = OBSManager()
            # manager.start_obs_process()
            # ... samd
            input("\nPress ENTER to return to menu...")
            
        elif option == '2':
            print("\n[Client] Connection Parameters:")
            host_ip = input("HOST IP: ").strip()
            
            print(f"\n[Client] Connecting to {host_ip}...")
            # Logica ta de client, ex: run_client(host_ip)
            input("\nPress ENTER to return to menu...")
            
        elif option == '0':
            print("\nClosing application. Goodbye!")
            sys.exit(0)
            
        else:
            print("\n[!] Invalid option. Please try again.")
            input("Press ENTER to return to menu...")

if __name__ == "__main__":
    run_menu()