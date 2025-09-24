# START:SOUND_MANAGER_IMPORTS
import pygame
# END:SOUND_MANAGER_IMPORTS

# START:SOUND_MANAGER_CLASS
class SoundManager:
    """ Manages game music and sound effects. """

    def __init__(self):
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        pygame.mixer.music.set_volume(self.music_volume)
        self.music = {
            "exploration": "background_music.ogg",
            "battle": "battle_music.ogg"
        }

    def load_music(self, track_name):
        """ Loads and prepares music for playback. """
        file_path = self.music.get(track_name)
        if file_path:
            try:
                pygame.mixer.music.load(file_path)
            except pygame.error as e:
                print(f"Cannot load music file: {e}")

    def play_music(self):
        """ Plays the loaded music in a loop. """
        pygame.mixer.music.play(-1) # -1 means loop indefinitely

    def stop_music(self):
        """ Stops the current music. """
        pygame.mixer.music.stop()

    def play_sfx(self, file_path):
        """ Plays a sound effect once. """
        try:
            sfx = pygame.mixer.Sound(file_path)
            sfx.set_volume(self.sfx_volume)
            sfx.play()
        except pygame.error as e:
            print(f"Cannot load sound effect file: {e}")
# END:SOUND_MANAGER_CLASS