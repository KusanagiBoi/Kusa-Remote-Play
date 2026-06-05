import socket
import json
import evdev
from evdev import ecodes as e

class InputReceiver:
    def __init__(self, port=9999):
        self.port = port
        self.ip = "0.0.0.0"
        self.ui = None
        self.sock = None
        self.capacitati = {
            e.EV_KEY: [
                e.BTN_A, e.BTN_B, e.BTN_X, e.BTN_Y,
                e.BTN_TL, e.BTN_TR, e.BTN_TL2, e.BTN_TR2,
                e.BTN_SELECT, e.BTN_START, e.BTN_MODE,
                e.BTN_THUMBL, e.BTN_THUMBR,
                e.BTN_DPAD_UP, e.BTN_DPAD_DOWN, e.BTN_DPAD_LEFT, e.BTN_DPAD_RIGHT
            ],
            e.EV_ABS: [
                (e.ABS_X, evdev.AbsInfo(value=0, min=-32768, max=32767, fuzz=0, flat=0, resolution=0)),
                (e.ABS_Y, evdev.AbsInfo(value=0, min=-32768, max=32767, fuzz=0, flat=0, resolution=0)),
                (e.ABS_RX, evdev.AbsInfo(value=0, min=-32768, max=32767, fuzz=0, flat=0, resolution=0)),
                (e.ABS_RY, evdev.AbsInfo(value=0, min=-32768, max=32767, fuzz=0, flat=0, resolution=0)),
                (e.ABS_Z, evdev.AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),    
                (e.ABS_RZ, evdev.AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),   
                (e.ABS_HAT0X, evdev.AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)), 
                (e.ABS_HAT0Y, evdev.AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0))  
            ]
        }

    def start(self):
        try:
            self.ui = evdev.UInput(self.capacitati, name="Kusa-Remote-Pad", vendor=0x045e, product=0x028e)
            print("[InputReceiver] Created virtual controller: Kusa-Remote-Pad")
        except evdev.uinput.UInputError as err:
            print(f"[Error] Could not create virtual controller: {err}")
            return

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        print(f"[InputReceiver] Listening for input on UDP/{self.port}...")

        try:
            while True:
                data, addr = self.sock.recvfrom(1024)
                try:
                    event = json.loads(data.decode('utf-8'))
                    
                    tip = event['type']
                    cod = event['code']
                    valoare = event['value']

                    # TRANSLATION LAYER: D-PAD
                    if tip == e.EV_ABS:
                        if cod == e.ABS_HAT0X:
                            self.ui.write(e.EV_KEY, e.BTN_DPAD_LEFT, 1 if valoare == -1 else 0)
                            self.ui.write(e.EV_KEY, e.BTN_DPAD_RIGHT, 1 if valoare == 1 else 0)
                            self.ui.syn()
                            continue 
                        elif cod == e.ABS_HAT0Y:
                            self.ui.write(e.EV_KEY, e.BTN_DPAD_UP, 1 if valoare == -1 else 0)
                            self.ui.write(e.EV_KEY, e.BTN_DPAD_DOWN, 1 if valoare == 1 else 0)
                            self.ui.syn()
                            continue

                    self.ui.write(tip, cod, valoare)
                    self.ui.syn()
                    
                except json.JSONDecodeError:
                    pass
                except KeyError:
                    pass
        except KeyboardInterrupt:
            # Prindem Ctrl+C ca sa stim cand iesim curat din sesiune
            print("\n[InputReceiver] Input reception stopped.")
        finally:
            self.cleanup()

    def cleanup(self):
        if self.ui:
            self.ui.close()
        if self.sock:
            self.sock.close()
        print("[InputReceiver] Resources cleaned up. Goodbye!")