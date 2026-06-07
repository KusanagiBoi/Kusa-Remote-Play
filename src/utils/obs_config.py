import json
import configparser
import subprocess
from pathlib import Path

def detect_gpu_encoder():
    try:
        result = subprocess.run(
            ["lspci"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.lower()
        
        if "nvidia" in output:
            print("[Hardware] NVIDIA GPU detected. Allocating NVENC encoder.")
            return "jim_nvenc", None
        elif "amd" in output or "radeon" in output:
            print("[Hardware] AMD GPU detected. Allocating VAAPI encoder.")
            return "ffmpeg_vaapi", "/dev/dri/renderD128"
        elif "intel" in output:
            print("[Hardware] Intel GPU detected. Allocating VAAPI encoder.")
            return "ffmpeg_vaapi", "/dev/dri/renderD128"
        else:
            print("[Hardware] GPU unidentified. Fallback to x264 (Software).")
            return "obs_x264", None
            
    except Exception as e:
        print(f"[Error] Could not verify hardware components: {e}. Fallback to x264.")
        return "obs_x264", None

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
        config.optionxform = str 
        config.read(global_ini_path)
        if 'Basic' in config and 'ProfileDir' in config['Basic']:
            profile_name = config['Basic']['ProfileDir']
            
    service_json_path = config_dir / "basic" / "profiles" / profile_name / "service.json"
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

    basic_ini_path = config_dir / "basic" / "profiles" / profile_name / "basic.ini"
    encoder_name, vaapi_device = detect_gpu_encoder()
    
    try:
        cfg = configparser.ConfigParser()
        cfg.optionxform = str
        
        if basic_ini_path.exists():
            cfg.read(basic_ini_path)
            
        if 'Output' not in cfg:
            cfg['Output'] = {}
        cfg['Output']['Mode'] = 'Advanced'
        
        if 'AdvOut' not in cfg:
            cfg['AdvOut'] = {}
            
        cfg['AdvOut']['Encoder'] = encoder_name
        cfg['AdvOut']['RecEncoder'] = encoder_name
        
        if vaapi_device:
            cfg['AdvOut']['VaapiDevice'] = vaapi_device
        elif 'VaapiDevice' in cfg['AdvOut']:
            del cfg['AdvOut']['VaapiDevice']
            
        with open(basic_ini_path, 'w') as f:
            cfg.write(f)
            
        print(f"[Setup] Configured OBS to use {encoder_name} encoder.")
    except Exception as e:
        print(f"[Error] Could not force hardware encoder in basic.ini: {e}")