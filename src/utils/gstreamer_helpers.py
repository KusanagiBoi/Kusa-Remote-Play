import subprocess
import platform

def check_gst_element(element_name):
    try:
        result = subprocess.run(
            ["gst-inspect-1.0", element_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_best_h264_decoder():
    arch = platform.machine().lower()
    
    if arch in ["aarch64", "armv7l", "arm"]:
        if check_gst_element("v4l2h264dec"):
            return "v4l2h264dec"
            
    elif arch in ["x86_64", "amd64"]:
        if check_gst_element("nvh264dec"):
            return "nvh264dec"
        elif check_gst_element("vaapih264dec"):
            return "vaapih264dec"
            
    return "avdec_h264"