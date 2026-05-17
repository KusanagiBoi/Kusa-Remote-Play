import subprocess
import sys

SRT_URL = "srt://0.0.0.0:8888?mode=listener"

# Modificat pentru a folosi flatpak-spawn și a rula MPV din afara sandbox-ului
cmd_mpv = [
    "flatpak-spawn",
    "--host",
    "flatpak",
    "run",
    "io.mpv.Mpv",
    SRT_URL,
    "--profile=low-latency",
    "--hwdec=auto",
    "--untimed",
    "--no-cache",
    "--fs"
]

print(f"Waiting for remote play feed from {SRT_URL}...")

try:
    player = subprocess.Popen(cmd_mpv)
    player.wait()
except KeyboardInterrupt:
    print("\nOpresc stream-ul...")
    player.terminate()
    sys.exit(0)
except FileNotFoundError:
    # FileNotFoundError va apărea acum doar dacă utilitarul flatpak-spawn lipsește din runtime-ul tău
    print("Eroare: Nu s-a putut executa flatpak-spawn. Asigură-te că rulezi codul dintr-un mediu Flatpak.")