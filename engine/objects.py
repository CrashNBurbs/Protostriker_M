#-------------------------------------------------------------------------------
# Name:        GameObjects.py
# Purpose:     Contains some useful and generic game object class (WIP)
#
# Author:      Will Taplin
#
# Created:     09/11/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pygame
from pygame.locals import *


class AnimatedSprite(pygame.sprite.Sprite):
    """ Enhanced version of pygame's sprite class
    sets up some common values for movement and frame animation.
    Update method will animate the sprites images at fps """
    def __init__(self,x, y, images, fps = 10, rows = False):
        pygame.sprite.Sprite.__init__(self)
        # load images and sounds
        self.images = images
        # initialize values for delays, timers, and movement
        self.delay = 1000 / fps  # m/s per frame, amount of delay for frame animation
        self.last_update = 0  # keep track of last animation update
        self.frame = 0
        self.timestep = 1 / 60.0

        if rows: # for multirow sprite sheets
            self.image = self.images[0][0]
        else: # single row sprite sheets
            self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.dx = x  # used to assign floating point values
        self.dy = y  # to rect x,y
        self.rect.x = x
        self.rect.y = y

    def update(self, current_time):
        # Animate the sprite by stepping through it's images
        # every self.delay m/s
        if current_time - self.last_update > self.delay:
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
            self.image = self.images[self.frame]
            self.last_update = current_time

    def handle_input(self, current_time):
        pass

class SpriteManager():
    """ Abstract class for sprite manager.
    self.sprite is intended to hold pygame sprite groups """
    def __init__(self):
        self.sprites = dict()

    def update(self):
        pass

    def draw(self, surface):
        # draw all sprites, in all groups
        # to surface
        for key in self.sprites.iterkeys():
            self.sprites[key].draw(surface)

    def add_group(self, group, key):
        # add a sprite group to self.sprites
        # with name key
        self.sprites[key] = group

    def add_sprite(self, sprite, group):
        # add a list of objects to group
        # group is a dictionary key
        self.sprites[group].add(sprite)




