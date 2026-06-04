import json
import configparser
from pathlib import Path

def force_enable_obs_websocket():
    print("[Setup] Forcing WebSocket activation in OBS...")
    
    config_dir = Path.home() / ".var/app/com.obsproject.Studio/config/obs-studio"
    plugin_config_dir = config_dir / "plugin_config" / "obs-websocket"
    config_json_path = plugin_config_dir / "config.json"
    
    if not plugin_config_dir.exists():
        plugin_config_dir.mkdir(parents=True, exist_ok=True)
        
    config_data = {
        "server_enabled": True,
        "server_port": 4455,
        "auth_required": False
    }
    
    try:
        if config_json_path.exists():
            with open(config_json_path, 'r') as f:
                data = json.load(f)
                data["server_enabled"] = True
                data["auth_required"] = False
                config_data = data
                
        with open(config_json_path, 'w') as f:
            json.dump(config_data, f, indent=4)
            
        print("[Setup] WebSocket activated successfully.")
    except Exception as e:
        print(f"[Error] Could not modify WebSocket config: {e}")

def force_configure_obs_stream(target_ip, target_port, latency):
    print(f"[Setup] Configuring OBS for SRT to {target_ip}:{target_port} with latency {latency}ms...")
    
    config_dir = Path.home() / ".var/app/com.obsproject.Studio/config/obs-studio"
    global_ini_path = config_dir / "global.ini"
    profile_name = "Untitled" 
    
    if global_ini_path.exists():
        config = configparser.ConfigParser()
        config.read(global_ini_path)
        if 'Basic' in config and 'ProfileDir' in config['Basic']:
            profile_name = config['Basic']['ProfileDir']
            
    service_json_path = config_dir / "basic" / "profiles" / profile_name / "service.json"
    
    # Construim URL-ul dinamic in functie de ce primeste functia
    srt_url = f"srt://{target_ip}:{target_port}?mode=caller&latency={latency}"
    
    service_data = {
        "settings": {
            "server": srt_url,
            "key": "" 
        },
        "type": "rtmp_custom" 
    }
    
    service_json_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(service_json_path, 'w') as f:
            json.dump(service_data, f, indent=4)
        print(f"[Setup] Configured SRT stream (URL: {srt_url}) in profile '{profile_name}'.")
    except Exception as e:
        print(f"[Error] Could not modify service.json: {e}")