import platform

def is_obs_host_supported():
    architecture = platform.machine().lower()
    if architecture not in ["x86_64", "amd64"]:
        return False
        
    return True