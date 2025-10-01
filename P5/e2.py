import vlc
import time
import os
import subprocess
import threading
import pyudev

# --- Configuración ---
username = "pi"  # <--- Cambia esto por tu nombre de usuario
pictures_path = f"/home/{username}/pictures/"

# --- Variables compartidas entre hilos ---
usb_detected_event = threading.Event()
usb_mount_point = [None]  # Usamos una lista para que sea mutable entre hilos

def get_mount_point(path):
    """Obtiene el punto de montaje de un dispositivo."""
    try:
        args = ["findmnt", "-unl", "-S", path]
        cp = subprocess.run(args, capture_output=True, text=True, check=True)
        return cp.stdout.strip().split(" ")[0]
    except (subprocess.CalledProcessError, IndexError):
        return None

def monitor_usb():
    """Vigila la conexión de dispositivos USB en un hilo separado."""
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='partition')

    print("Hilo monitor de USB iniciado. Esperando dispositivo...")
    for action, device in monitor:
        if action == 'add':
            print(f"Dispositivo USB detectado: {device.sys_name}")
            time.sleep(1) # Dar tiempo al sistema para registrar el dispositivo
            
            # Montar el dispositivo
            device_path = "/dev/" + device.sys_name
            subprocess.run(["udisksctl", "mount", "-b", device_path])
            
            # Obtener el punto de montaje
            mp = get_mount_point(device_path)
            if mp:
                print(f"Dispositivo montado en: {mp}")
                usb_mount_point[0] = mp
                usb_detected_event.set() # Activa la bandera para notificar al hilo principal
                break

def play_images_from_path(player, path):
    """Reproduce imágenes de una ruta específica en un bucle."""
    try:
        image_files = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.png'))]
    except FileNotFoundError:
        print(f"Error: El directorio no fue encontrado en {path}")
        return

    if not image_files:
        print(f"No se encontraron imágenes en {path}.")
        return

    while not usb_detected_event.is_set() if path == pictures_path else True:
        for image_file in image_files:
            # Si estamos en el bucle local y se detecta un USB, salimos
            if path == pictures_path and usb_detected_event.is_set():
                return
                
            full_path = os.path.join(path, image_file)
            media = vlc.Media(full_path)
            player.set_media(media)
            player.play()
            time.sleep(3)
            player.stop()

# --- Script Principal ---
player = vlc.MediaPlayer()

# Iniciar el hilo del monitor USB
monitor_thread = threading.Thread(target=monitor_usb)
monitor_thread.daemon = True  # Permite que el programa principal termine aunque el hilo siga activo
monitor_thread.start()

# Reproducir imágenes locales hasta que se detecte un USB
print("Iniciando presentación con imágenes locales...")
play_images_from_path(player, pictures_path)

# Si el evento fue activado, significa que se conectó un USB
if usb_detected_event.is_set():
    print("\nUSB detectado. Cambiando a la presentación de imágenes de la USB...")
    if usb_mount_point[0]:
        play_images_from_path(player, usb_mount_point[0])
    else:
        print("No se pudo obtener el punto de montaje del USB.")

print("Finalizando script.")