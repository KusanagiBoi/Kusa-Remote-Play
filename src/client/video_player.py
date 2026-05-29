import subprocess
import sys
from src.utils.gstreamer_helpers import get_best_h264_decoder

SRT_URL = "srt://0.0.0.0:8888?mode=listener"

def receive_stream():
    decoder = get_best_h264_decoder()
    print(f"[Video] Folosesc decodorul: {decoder}")
    
    cmd_gstreamer = [
        "gst-launch-1.0",
        "srtsrc", f"uri={SRT_URL}", "latency=0",
        "!", "tsdemux",
        "!", "h264parse",
        "!", decoder,
        "!", "waylandsink", "sync=false" 
    ]

    print(f"Waiting for remote play feed from {SRT_URL}...")

    try:
        player = subprocess.Popen(cmd_gstreamer)
        player.wait()
    except KeyboardInterrupt:
        print("\nOpresc stream-ul...")
        player.terminate()
        sys.exit(0)
    except FileNotFoundError:
        print("Eroare: GStreamer lipseste. Asigura-te ca dependentele sunt instalate.")

if __name__ == "__main__":
    receive_stream()