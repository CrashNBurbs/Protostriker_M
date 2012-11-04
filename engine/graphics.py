#-------------------------------------------------------------------------------
# Name:        Graphics
# Purpose:     Component of Engine, contains the images manager and
#              Viewport class
#
# Author:      Will Taplin
#
# Created:     02/07/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
import os

class ImageManager():
    """ loads all game images and font into a single dictionary
        call load_single for a single image, load_sliced_images for
        a sprite sheet
        filename - name of image file to load
        key - the ID for the image, or set of images
        w, h - width and height of individual frame (sprite sheet)
        rows - boolean for whether the sprite sheet has multiple rows or not
        colorkey - RGB value for transparency, - 1 will take color from top
                   left corner of image for transparency """

    def __init__(self):
        self.images = dict()  # dictionary of all images loaded
        self.font = self.load_font('prstartk.ttf', 8)

    def load_image(self, filename, colorkey = None):
        # call pygame image load function
        fullname = os.path.join('data', filename) # create platform independent path
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', filename
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:  # colorkey of -1 will get pixel at top left
                colorkey =  image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

    def load_sliced_images(self, filename, w, h, rows, colorkey):
        # slice up a sprite sheet
        # returns a list of pygame surfaces
        images = []
        master_image = self.load_image(filename, colorkey = colorkey)
        master_width, master_height = master_image.get_size()
        if rows:  # for images that have more than one row
            for j in range(int(master_height/h)):
                images.append([])  # add a new row to the list
                for i in range(int(master_width/w)):  # number of frames wide
                    images[j].append(master_image.subsurface((i*w,j*h,w,h)))  # add each frame, from left to right
        else: # for single row image sheets
            for i in range(int(master_width/w)):
                images.append(master_image.subsurface((i*w,0,w,h)))
        return images

    def load_single(self, filename, key, colorkey = None):
        # loads a single image into the image manager
        image = self.load_image(filename, colorkey)
        self.images[key] = image

    def load_sheet(self, filename, key, w, h, rows = True, colorkey = None):
        # loads an image sheet into the image manager
        # load_sliced_images returns the individual frames or tiles
        images = self.load_sliced_images(filename, w, h, rows, colorkey)
        self.images[key] = images

    def load_font(self, name, size):
        fullname = os.path.join('Data', name)
        try:
            font = pygame.font.Font(fullname, size)
        except pygame.error, message:
            print 'Cannot load font:', name
            raise SystemExit, message
        return font

    def get_image(self, key):
        # accessor method for images
        # use to assign a sprites image attribute
        return self.images[key]

    def get_font(self):
        return self.font

class Viewport():
    """ This class creates a viewport that is the size
    of the screen, from a larger background image to
     enable scrolling"""
    def __init__(self, background, player, auto_scroll = True):
        self.background = background
        self.player = player
        self.auto_scroll = auto_scroll
        self.width = 320 # width of screen
        self.height = 240 # height of screen
        self.coordinate = 0  # left edge of viewport
        self.level_pos = 0
        self.minScroll = 0 # max value for left scrolling
        self.maxScroll = self.background.get_width() - 320 # max for right
        self.advance_velocity = 100  # speed of scroll
        self.timestep = 1 / 60.0  # target frame rate
        self.vp = self.background.subsurface((self.coordinate, 0, self.width, self.height))

    def update(self):
        if self.auto_scroll: # background scrolls on its own
            self.coordinate += self.advance_velocity * self.timestep
            self.level_pos += self.advance_velocity * self.timestep
        #else:  # background scrolls as a result of the player passing a point on screen
            #if self.player.rect.right >= 130 and \
            #game.input_manager.is_held('RIGHT') and \
            #not self.player.kicking and not self.player.punching:
                #self.coordinate += self.advance_velocity * self.timestep

        # loop image
        if self.coordinate > self.maxScroll:
                self.coordinate = 0

    def draw(self, screen):
        # create new subsurface from updated coordinate
        # draw it to the screen
        self.vp = self.background.subsurface((self.coordinate, 0, self.width, self.height))
        screen.blit(self.vp, (0,0))
