import obsws_python as obs
import subprocess
import time
from src.utils.env_spawn import spawn  # Importam functia de adaptare la mediu

class OBSManager:
    def __init__(self, host="localhost", port=4455, password=""):
        self.host = host
        self.port = port
        self.password = password
        self.client = None

    def launch_obs(self):
        print("[OBS Manager] Pornesc OBS in background (minimized)...")
        try:
            # Construim comanda adaptiva folosind functia ta
            base_cmd = ["flatpak", "run", "com.obsproject.Studio", "--minimize-to-tray"]
            adaptive_cmd = spawn() + base_cmd
            
            subprocess.Popen(
                adaptive_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Ii dam 4 secunde sa isi incarce modulele si sa deschida portul pe retea
            time.sleep(4) 
            return True
        except Exception as e:
            print(f"[Error] Failed to launch OBS: {e}")
            return False

    def connect(self):
        print("[OBS Manager] Incerc sa ma conectez la serverul WebSocket...")
        try:
            self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
            print("[OBS Manager] Conexiune stabilita cu succes la OBS!")
            return True
        except Exception:
            print("[OBS Manager] OBS-ul nu raspunde. Il deschid automat acum...")
            self.launch_obs()
            
            # A doua incercare de conectare, dupa ce am fortat pornirea
            try:
                self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
                print("[OBS Manager] Conexiune stabilita cu succes dupa auto-launch!")
                return True
            except Exception as e2:
                print(f"[Error] Failed to connect to OBS even after auto-launch: {e2}")
                return False

    def start_stream(self):
        if not self.client:
            print("[Error] No active connection to OBS. Please call connect() first.")
            return False
            
        try:
            self.client.start_stream()
            print("[OBS Manager] Start Stream command sent!")
            return True
        except Exception as e:
            print(f"[Error] Failed to start stream: {e}")
            return False

    def stop_stream(self):
        if not self.client:
            return False
            
        try:
            self.client.stop_stream()
            print("[OBS Manager] Stream stopped.")
            return True
        except Exception as e:
            print(f"[Error] Failed to stop stream: {e}")
            return False

    def disconnect(self):
        if self.client:
            self.client = None
            print("[OBS Manager] Connection closed.")