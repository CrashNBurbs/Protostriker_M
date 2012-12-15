#-------------------------------------------------------------------------------
# Name:        Sound
# Purpose:     Component of Engine, contains the sound manager
#
# Author:      Will Taplin
#
# Created:     05/07/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
import os

class SoundManager():
    """ This class handles the loading and playback of sounds
        and music.  All sound effects are stored in a single dictionary.
        All music is streamed directly from the file """
    def __init__(self):
        self.sounds = dict()  # dictionary of all sound effects loaded

    def load(self, filename, volume = 0.5):
        # load a sound for playback
        fullname = os.path.join('res', 'sound_effects', filename)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print 'Cannot load sound:', filename
            raise SystemExit, message
        sound.set_volume(volume)
        return sound

    def load_sound(self, filename, key, volume = 0.5):
        # loads a single image into the image manager
        sound = self.load(filename, volume)
        self.sounds[key] = sound

    def get_sound(self, key):
        return self.sounds[key]

    def unload_sound(self, key):
        # remove a sound from the sound manager
        del self.sounds[key]

    def play_music(self, filename, loops = -1):
        # play selected music, if already playing, stop current song, play new one
        # loops song infinitely by default
        try:
            song = os.path.join('res', 'music', filename)
        except pygame.error, message:
            print 'Cannot play music: ', filename
            raise SystemExit, message
        if song:
            if pygame.mixer.music.get_busy == False:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play(loops)
            else:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(song)
                pygame.mixer.music.play(loops)

    def music_control(self, control, fade_time = 1000):
        # various music controls
        if control == "stop":
                pygame.mixer.music.stop()
        elif control == "pause":
                pygame.mixer.music.pause()
        elif control == "unpause":
                pygame.mixer.music.unpause()
        elif control == "fade":
                pygame.mixer.music.fadeout(fade_time)
