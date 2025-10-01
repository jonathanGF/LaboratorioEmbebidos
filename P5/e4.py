import vlc
import time
import os
import RPi.GPIO as GPIO

# --- Configuración ---
username = "pi"  # <--- Cambia esto por tu nombre de usuario
media_path = f"/home/{username}/pictures/" # Directorio con las imágenes o videos

# Mapeo de pines GPIO según la práctica [cite: 144]
PIN_NEXT = 3
PIN_PREV = 2
PIN_STOP = 4
PIN_PAUSE_RESUME = 17
PIN_VOL_UP = 27
PIN_VOL_DOWN = 22

# --- Inicialización del reproductor y la lista de medios ---
instance = vlc.Instance()
player = instance.media_player_new()
media_list = instance.media_list_new()
list_player = instance.media_list_player_new()
list_player.set_media_player(player)

media_files = [os.path.join(media_path, f) for f in os.listdir(media_path) if f.lower().endswith(('.jpg', '.png', '.mp4'))]
for mf in media_files:
    media_list.add_media(instance.media_new(mf))

list_player.set_media_list(media_list)

# --- Funciones de Callback para los botones ---
def handle_next(pin):
    print("Botón -> Siguiente")
    list_player.next()

def handle_prev(pin):
    print("Botón -> Anterior")
    list_player.previous()

def handle_stop(pin):
    print("Botón -> Detener")
    list_player.stop()

def handle_pause_resume(pin):
    print("Botón -> Pausa/Reanudar")
    list_player.pause() # Esta función alterna entre pausa y reproducción

def handle_vol_up(pin):
    current_volume = player.audio_get_volume()
    new_volume = min(current_volume + 10, 100) # Sube 10, con un tope de 100
    player.audio_set_volume(new_volume)
    print(f"Botón -> Vol+ (Volumen: {new_volume}%)")

def handle_vol_down(pin):
    current_volume = player.audio_get_volume()
    new_volume = max(current_volume - 10, 0) # Baja 10, con un tope de 0
    player.audio_set_volume(new_volume)
    print(f"Botón -> Vol- (Volumen: {new_volume}%)")


# --- Configuración de GPIO ---
GPIO.setmode(GPIO.BCM) # Usar numeración BCM
pins = [PIN_NEXT, PIN_PREV, PIN_STOP, PIN_PAUSE_RESUME, PIN_VOL_UP, PIN_VOL_DOWN]

# Configurar cada pin como entrada con resistencia pull-up
for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Asignar eventos a cada pin (interrupciones)
GPIO.add_event_detect(PIN_NEXT, GPIO.FALLING, callback=handle_next, bouncetime=300)
GPIO.add_event_detect(PIN_PREV, GPIO.FALLING, callback=handle_prev, bouncetime=300)
GPIO.add_event_detect(PIN_STOP, GPIO.FALLING, callback=handle_stop, bouncetime=300)
GPIO.add_event_detect(PIN_PAUSE_RESUME, GPIO.FALLING, callback=handle_pause_resume, bouncetime=300)
GPIO.add_event_detect(PIN_VOL_UP, GPIO.FALLING, callback=handle_vol_up, bouncetime=300)
GPIO.add_event_detect(PIN_VOL_DOWN, GPIO.FALLING, callback=handle_vol_down, bouncetime=300)

# --- Bucle Principal ---
try:
    print("Controles GPIO activados. Iniciando reproducción...")
    list_player.play()
    # El script se mantiene en espera mientras las interrupciones hacen el trabajo
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nSaliendo del programa.")

finally:
    list_player.stop()
    GPIO.cleanup() # Limpiar la configuración de los pines GPIO al salir