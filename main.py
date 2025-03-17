from Devices.Logitech.keyboard import Keyboard
import time

from Spotify.colour_extract import ColourExtract
from Spotify.spotify import Spotify

is_running = True
previous_song = None

def change_colour():
    global previous_song
    global current_song

    previous_song = current_song
    colour = ColourExtract.get_colour(current_song.album.images[0]["url"])
    device.set_colour(colour)

if __name__ == "__main__":
    device = Keyboard()
    spotify = Spotify()
    spotify.refresh()

    while is_running:
        current_song = spotify.get_currently_playing()
        if previous_song is None:
            change_colour()
            continue

        if current_song is None:
            time.sleep(1)
            continue

        if current_song.id != previous_song.id:
            change_colour()

        time.sleep(1)

