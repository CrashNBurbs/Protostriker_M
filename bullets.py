#------------------------------------------------------------------------------
# Name:        Bullets.py
# Purpose:     Contains the classes used to create all bullets
#              in the game
#
# Author:      Will Taplin
#
# Created:     11/12/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
import engine
import math
from engine.system import TIMESTEP
from engine.system import SCREEN_RECT

class Bullet(pygame.sprite.Sprite):
    """ Abstract class for a bullet """
    def __init__(self, x, y, angle, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.dx = self.rect.x
        self.dy = self.rect.y
        self.speed = 0
        self.angle = angle
        self.bounds = SCREEN_RECT
        self.hitbox = pygame.Rect(self.dx, self.dy, 0, 0)
        self.hb_offsetx = 0
        self.hb_offsety = 0
        self.destroyable = True


    def update(self):
        pass

class BasicBullet(Bullet):
    """ Player bullet class, sub-class of Bullet
    Object moves horizontally from left to right for the duration
    it is on screen """
    def __init__(self, x, y, angle, image):
        Bullet.__init__(self, x, y, angle, image)
        self.speed = 400
        self.hb_offsety = 2
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 8, 4)
     
    def update(self, *args):
        # move bullet at self.speed pixels/sec
        self.dx += self.speed * TIMESTEP

        # update the rect and hitbox
        self.rect.x = self.dx
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # kill if offscreen
        if self.rect.right > self.bounds.right:
            self.kill()

class EnemyBullet(Bullet):
    """ Enemy bullet class, sub-class of Bullet.
    Object moves horizontally from right to left for the duration
    it is on screen """
    def __init__(self, x, y, angle, image):
        Bullet.__init__(self, x, y, angle, image)
        self.speed = 135
        self.hb_offsetx = 1
        self.hb_offsety = 1
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 6, 6)
   
    def update(self, *args):
        # move bullet at self.speed/sec
        self.dx -= self.speed * TIMESTEP

        # update the rect and hitbox
        self.rect.x = self.dx
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # kill if offscreen
        if self.rect.left < self.bounds.left:
            self.kill()

class SpreaderBullet(Bullet):
    """ bullet for the spreader gun, can travel at an angle """
    def __init__(self, x, y, angle, image):
        Bullet.__init__(self, x, y, angle, image)
        self.speed = 300
        self.radians = -self.angle * math.pi / 180
        self.hb_offsetx = 1
        self.hb_offsety = 1
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 6, 6)
      
    def update(self, *args):
        # calculate change in x,y
        self.dx += (math.cos(self.radians) * self.speed) * TIMESTEP
        self.dy += (math.sin(self.radians) * self.speed) * TIMESTEP

        # update the rects
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # check for screen bounds, kill if offscreen
        if not self.bounds.contains(self.rect):
            self.kill()

class ReverseFireBullet(SpreaderBullet):
    """ Bullet for reverse shot gun, can travel at an angle """

    def __init__(self, x, y, angle, image):
        SpreaderBullet.__init__(self, x, y, angle, image)
        self.speed = 400
        self.hb_offsetx = 0
        self.hb_offsety = 2
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 8, 4)
        self.center = self.rect.center
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def update(self, *args):
        SpreaderBullet.update(self, *args)

        if self.angle == 220:
            self.hitbox.y += 3

class LaserBeam(pygame.sprite.Sprite):
    """ Laser Beam bullet - an expanding shot that stays attached to the
        player and lasts for self.duration before disapearing """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 1
        self.image = pygame.Surface((self.width, 4))
        self.image.fill((0,136,148))
        pygame.draw.line(self.image, (0,64,88), (0,0),(self.width,0))
        pygame.draw.line(self.image, (0,64,88), (0,3),(self.width,3)) 
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.speed = 1000
        self.duration = 650
        self.destroyable = False
        self.shot_time = pygame.time.get_ticks()
        

    def update(self, *args):
        current_time = args[0]
        player_rect = args[1]
        
        # increase the length of the beam while it has not hit the edge of
        # the screen
        if self.rect.right < SCREEN_RECT.width:
            self.width += self.speed * TIMESTEP
        else:  # beam has hit the edge of the screen, shorten if necessary
            self.width = SCREEN_RECT.width - self.rect.x
            # keep width at least 1
            if self.width < 1:
                self.width = 1

        # scale the image
        self.image = pygame.transform.scale(self.image, (int(self.width), 4))

        # get new rect, set x and y
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.rect.x = player_rect.right - 6
        self.rect.y = player_rect.centery - 2

        # kill beam after self.duration
        if current_time - self.shot_time > self.duration:
            self.kill()

class Explosion(engine.objects.AnimatedSprite):
    """ Explosion animation """

    def __init__(self, x, y, images):
        engine.objects.AnimatedSprite.__init__(self,x,y,images)
        self.hitbox = None

    def update(self, *args):
        current_time = args[0]
        # Animate through all frames once, then kill sprite
        if current_time - self.last_update > self.delay:
            self.frame += 1
            if self.frame >= len(self.images):
                self.frame = 0
                self.kill()
            self.image = self.images[self.frame]
            self.last_update = current_time

class Shrapnel(Bullet):
    """ Shrapnel object """
    def __init__(self, x, y, angle, images):
        Bullet.__init__(self, x, y, angle, images[0])
        self.image = images[angle / 45]
        self.radians = -self.angle * math.pi / 180  
        self.hb_offsetx = 1
        self.hb_offsety = 1
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 6, 6)
        self.speed = 35

    def update(self, *args):
        # calculate change in x,y
        self.dx += (math.cos(self.radians) * self.speed) * TIMESTEP
        self.dy += (math.sin(self.radians) * self.speed) * TIMESTEP

        # update the rects
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # check for screen bounds, kill if offscreen
        if not self.bounds.contains(self.rect):
            self.kill()
