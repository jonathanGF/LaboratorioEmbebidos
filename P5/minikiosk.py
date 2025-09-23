import vlc
player = vlc.MediaPlayer()
video = vlc.Media(’/home/pi/videos/video.mp4’)
player.set_media(video)
player.play()
while player.is_playing:
    time.sleep(0)