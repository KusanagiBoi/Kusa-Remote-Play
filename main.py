from src.client.video_player import receive_stream
#receive_stream()

# Importi clasa exact de unde ai salvat-o
from src.host.obs_manager import OBSManager

'''def testeaza_obs_simplu():
    print("--- Test minimal OBS ---")
    
    # 1. Creezi instanta clasei si o asignezi unei variabile
    manager_obs = OBSManager()
    
    # 2. Apelezi functia din clasa. 
    # Asta va incerca sa se conecteze, va vedea ca OBS e oprit si ii va da launch automat.
    manager_obs.connect()
    
    # 3. Tii scriptul in viata ca sa apuci sa verifici daca a pornit OBS-ul in system tray
    input("\n[Test] OBS ar trebui sa fie pornit in fundal. Apasa ENTER pentru a deconecta scriptul...")
    
    # 4. Apelezi functia de deconectare
    manager_obs.disconnect()
    print("Test finalizat. Poti inchide OBS-ul manual daca a ramas in tray.")

if __name__ == "__main__":
    testeaza_obs_simplu()
'''