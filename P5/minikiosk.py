import vlc
import time
import os

# --- Configuración ---
# Asegúrate de cambiar "pi" por tu nombre de usuario si es diferente
username = "teamvip"
video_path = f"/home/{username}/videos/video.mp4"
pictures_path = f"/home/{username}/pictures/"

# --- Ejecución ---
player = vlc.MediaPlayer()

print("Reproduciendo video por 10 segundos...")
video_media = vlc.Media(video_path)
player.set_media(video_media)
player.play()
time.sleep(10)
player.stop()

print("Iniciando presentación de imágenes...")
try:
    image_files = [f for f in os.listdir(pictures_path) if f.lower().endswith(('.jpg', '.png'))]
except FileNotFoundError:
    image_files = []

if not image_files:
    print(f"No se encontraron imágenes en {pictures_path}. Finalizando.")
else:
    while True:
        for image_file in image_files:
            image_media = vlc.Media(os.path.join(pictures_path, image_file))
            player.set_media(image_media)
            player.play()
            time.sleep(3)
            player.stop()

