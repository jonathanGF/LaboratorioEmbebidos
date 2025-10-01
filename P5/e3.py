import vlc
import time

# --- Configuración ---
username = "pi" # <--- Cambia esto por tu nombre de usuario
video_path = f"/home/{username}/videos/video.mp4"

# --- Script Principal ---
player = vlc.MediaPlayer()
media = vlc.Media(video_path)
player.set_media(media)

print("Iniciando video con control de volumen (20 segundos en total)...")
player.play()

# 1. Fade-in de 5 segundos (Volumen 0 a 100)
print("Fase 1: Fade-in (0% -> 100%)")
player.audio_set_volume(0)
for volume in range(101):
    player.audio_set_volume(volume)
    time.sleep(0.05) # 5 segundos / 100 pasos

# 2. Volumen máximo durante 10 segundos
print("Fase 2: Volumen máximo")
player.audio_set_volume(100)
time.sleep(10)

# 3. Fade-out de 5 segundos (Volumen 100 a 0)
print("Fase 3: Fade-out (100% -> 0%)")
for volume in range(100, -1, -1):
    player.audio_set_volume(volume)
    time.sleep(0.05) # 5 segundos / 100 pasos

player.stop()
print("Reproducción finalizada.")