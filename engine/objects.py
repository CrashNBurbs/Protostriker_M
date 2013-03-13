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
import graphics
import system 
from pygame.locals import *
from system import SCREEN_RECT

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

        if rows: # for multirow sprite sheets
            self.image = self.images[0][0]
        else: # single row sprite sheets
            self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = self.rect.x # used to assign floating point values
        self.dy = self.rect.y  # to rect x,y


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
        for key in self.draw_order:
            self.sprites[key].draw(surface)

    def add_group(self, group, key):
        # add a sprite group to self.sprites
        # with name key
        self.sprites[key] = group

    def add_sprite(self, sprite, group):
        # add a list of objects to group
        # group is a dictionary key
        self.sprites[group].add(sprite)

class EventState(system.State):
    """ A multipurpose state that will display centered text for duration,
        play optional music, fade out, and change state
        to to_state after fade """

    def __init__(self, game, text, music, to_state, duration = 5000):
        system.State.__init__(self, game)
        self.duration = duration
        self.text = text
        self.font_height = game.font.get_height()
        self.lines = []
        self.music = music
        self.to_state = to_state
        
    
    def activate(self, transition):
        system.State.activate(self, transition)

        # pause interpolated draw, stop music create render from text, 
        # centered
        self.last_update = pygame.time.get_ticks()
        self.game.paused = True
        self.game.sound_manager.music_control('stop')
        for line in self.text:
            self.render = self.game.font.render(line, False, 
                                              self.game.text_color)
            self.lines.append(self.render)

    def update(self):
        system.State.update(self)

        current_time = pygame.time.get_ticks()

        # after duration start transitioning off
        if current_time - self.last_update > self.duration:
            self.transition_off(graphics.FadeAnimation("out"))
            self.last_update = current_time

        # after transition change state to self.to_state
        if self.done_exiting:
            self.game.change_state(self.to_state, graphics.FadeAnimation("in"))

    def draw(self, screen):
        
        self.render_y = (SCREEN_RECT.height - self.font_height * len(self.lines)) / 2

        for line in self.lines:
            self.render_x = (SCREEN_RECT.width - line.get_width()) / 2
            
            screen.blit(line, (self.render_x, self.render_y))
            self.render_y += 10

        if self.transitioning:
            self.transition.draw(screen)



