import obsws_python as obs
import subprocess
import time
import os
from src.utils.env_spawn import spawn  # Importam functia de adaptare la mediu

class OBSManager:
    def __init__(self, host="localhost", port=4455, password=""):
        self.host = host
        self.port = port
        self.password = password
        self.client = None

    def launch_obs(self):
        print("[OBS Manager] Starting OBS Studio...")
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
        print("[OBS Manager] Trying to connect to the WebSocket server...")
        try:
            self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
            print("[OBS Manager] Successfully connected to OBS!")
            return True
        except Exception:
            print("[OBS Manager] OBS-ul nu raspunde. Il deschid automat acum...")
            self.launch_obs()
            
            # A doua incercare de conectare, dupa ce am fortat pornirea
            try:
                self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password)
                print("[OBS Manager] Successfully connected to OBS after auto-launch!")
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

    def setup_display_capture(self):
        if not self.client:
            print("[Error] No active connection to OBS. Please call connect() first.")
            return False
            
        
        # Citim tipul sesiunii direct din variabilele de mediu ale Linux-ului
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
        
        if session_type == "wayland" or os.environ.get("WAYLAND_DISPLAY"):
            capture_kind = "pipewire-desktop-capture-source"
        else:
            capture_kind = "xshm_input" # Fallback curat pentru X11

        try:
            resp = self.client.get_current_program_scene()
            scene_name = resp.current_program_scene_name
            
            items_resp = self.client.get_scene_item_list(scene_name)
            source_name = "KusaAutoScreen"
            
            for item in items_resp.scene_items:
                if item['sourceName'] == source_name:
                    print(f"[OBS Manager] Source '{source_name}' already exists. Skipping creation.")
                    return True
                    
            print(f"[OBS Manager] Adding ({capture_kind}) to scene '{scene_name}'...")
            self.client.create_input(
                scene_name,
                source_name,
                capture_kind, 
                {}, 
                True 
            )
            print("[OBS Manager] Display capture source added successfully!")
            return True
            
        except Exception as e:
            print(f"[Error] Failed to add display capture source: {e}")
            return False