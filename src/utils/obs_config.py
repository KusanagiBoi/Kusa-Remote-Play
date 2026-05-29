import json
from pathlib import Path

def force_enable_obs_websocket():
    print("[Setup] Forteaza activarea serverului de WebSocket in OBS...")
    
    # Calea specifica pentru OBS-ul din Flatpak (Bazzite)
    config_dir = Path.home() / ".var/app/com.obsproject.Studio/config/obs-studio"
    plugin_config_dir = config_dir / "plugin_config" / "obs-websocket"
    config_json_path = plugin_config_dir / "config.json"
    
    # Ne asiguram ca structura de foldere exista
    if not plugin_config_dir.exists():
        plugin_config_dir.mkdir(parents=True, exist_ok=True)
        
    # Setarile standard: activat, port 4455, fara parola pentru teste locale
    config_data = {
        "server_enabled": True,
        "server_port": 4455,
        "auth_required": False
    }
    
    try:
        # Daca fisierul exista deja, il citim si doar suprascriem flag-urile esentiale
        if config_json_path.exists():
            with open(config_json_path, 'r') as f:
                data = json.load(f)
                data["server_enabled"] = True
                data["auth_required"] = False
                config_data = data
                
        # Salvam setarile inapoi
        with open(config_json_path, 'w') as f:
            json.dump(config_data, f, indent=4)
            
        print("[Setup] WebSocket activat cu succes. OBS-ul o sa citeasca flag-ul la pornire.")
    except Exception as e:
        print(f"[Eroare] Nu am putut modifica fisierul de config al OBS-ului: {e}")
