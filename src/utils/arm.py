import platform

def is_obs_host_supported():
    # Verificam arhitectura
    arhitectura = platform.machine().lower()
    if arhitectura not in ["x86_64", "amd64"]:
        return False
        
    return True

print(is_obs_host_supported())