import obsws_python as obs
import subprocess
import time
from src.utils.env_spawn import spawn

class OBSManager:
    def __init__(self, host="localhost", port=4455, password=""):
        self.host = host
        self.port = port
        self.password = password
        self.client = None

    def launch_obs(self):
        print("[OBS Manager] Starting OBS Studio...")
        try:
            base_cmd = ["flatpak", "run", "com.obsproject.Studio", "--minimize-to-tray"]
            adaptive_cmd = spawn() + base_cmd
            
            subprocess.Popen(
                adaptive_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
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
            print("[OBS Manager] OBS is not responding. Auto-launching now...")
            self.launch_obs()
            
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
            print("[Error] No active connection to OBS.")
            return False
            
        import time
        import os
        
        time.sleep(2)
        
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
        capture_kind = "pipewire-desktop-capture-source" if session_type == "wayland" else "xshm_input"

        try:
            resp = self.client.get_current_program_scene()
            scene_name = resp.current_program_scene_name
            
            items_resp = self.client.get_scene_item_list(scene_name)
            for item in items_resp.scene_items:
                if item['sourceName'] == "KusaAutoScreen":
                    return True
            
            self.client.create_input(
                scene_name,
                "KusaAutoScreen",
                capture_kind, 
                {"capture_cursor": True}, 
                True 
            )
            print("[OBS Manager] Capture source added successfully!")
            return True
            
        except Exception as e:
            print(f"[Warning] Capture injection failed (plugin might not be ready yet): {e}")
            return False