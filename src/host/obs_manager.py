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
            print(f"[Eroare OBS] Nu am putut lansa procesul: {e}")
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
                print(f"[Eroare OBS] Tot nu m-am putut conecta nici dupa auto-launch: {e2}")
                return False

    def start_stream(self):
        if not self.client:
            print("[Eroare OBS] Nu exista o conexiune activa. Apeleaza connect() intai.")
            return False
            
        try:
            self.client.start_stream()
            print("[OBS Manager] Comanda de Start Stream a fost trimisa!")
            return True
        except Exception as e:
            print(f"[Eroare OBS] Nu am putut porni stream-ul. E setat corect encoderul? Detalii: {e}")
            return False

    def stop_stream(self):
        if not self.client:
            return False
            
        try:
            self.client.stop_stream()
            print("[OBS Manager] Stream-ul a fost oprit.")
            return True
        except Exception as e:
            print(f"[Eroare OBS] Nu am putut opri stream-ul: {e}")
            return False

    def disconnect(self):
        if self.client:
            self.client = None
            print("[OBS Manager] Conexiunea WebSocket a fost inchisa.")