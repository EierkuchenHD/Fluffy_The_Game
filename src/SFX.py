import sys
import pygame
import os

class SFX:
    def __init__(self):
        pygame.mixer.init()
        if getattr(sys, 'frozen', False):
            # Running in a bundle
            script_dir = sys._MEIPASS
        else:
            # Running as a script
            script_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            self.jump_sound = pygame.mixer.Sound(os.path.join(script_dir, "data", "boing.ogg"))
        except FileNotFoundError:
            raise FileNotFoundError("The sound file 'boing.ogg' is missing.")

    def play_jump_sound(self):
        self.jump_sound.play()
