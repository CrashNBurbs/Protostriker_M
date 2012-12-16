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

class Bullet(pygame.sprite.Sprite):
    """ Abstract class for a bullet """
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.dx = x
        self.dy = y
        self.rect.left = self.dx
        self.rect.centery = self.dy
        self.speed = 0
        self.bounds = engine.system.SCREEN_RECT
        self.hitbox = pygame.Rect(self.dx, self.dy, 0, 0)
        self.hb_offsetx = 0
        self.hb_offsety = 0


    def update(self, current_time):
        pass

class BasicBullet(Bullet):
    """ Player bullet class, sub-class of Bullet
    Object moves horizontally from left to right for the duration
    it is on screen """
    def __init__(self, x, y, image):
        Bullet.__init__(self, x, y, image)
        self.speed = 400
        self.hitbox = pygame.Rect(self.dx,self.dy,8,3)

    def update(self, current_time):
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
    def __init__(self, x, y, image):
        Bullet.__init__(self, x, y, image)
        self.speed = 135
        self.hitbox = pygame.Rect(self.dx,self.dy,6,6)
        self.hb_offsetx = 1
        self.hb_offsety = 1

    def update(self, current_time):
        # move bullet at self.speed/sec
        self.dx -= self.speed * TIMESTEP

        # update the rect and hitbox
        self.rect.x = self.dx
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # kill if offscreen
        if self.rect.left < self.bounds.left:
            self.kill()

class SpreaderBullet(EnemyBullet):
    """ bullet for the spreader gun """
    def __init__(self, x, y, angle, image):
        EnemyBullet.__init__(self, x, y, image)
        self.speed = 300
        self.diag_speed = self.speed / math.sqrt(2)
        self.angle = angle
        self.hitbox = pygame.Rect(self.dx,self.dy,6,6)
        self.hb_offsetx = 1
        self.hb_offsety = 1
        self.ddx = self.dx
        self.ddy = self.dy

    def update(self, current_time):
        
        # convert degrees to radians
        radians = self.angle * math.pi / 180

        # calculate path for diagonal up
        if self.angle <= 90:
            self.ddx = (math.cos(radians))
            self.ddy = -(math.sin(radians))
        # calculate path for diagonal down
        elif self.angle >= 270:
            self.ddx = (math.cos(radians))
            self.ddy = -(math.sin(radians))
        else: # self.angle == 0
            self.ddx = (math.cos(radians))
            self.ddy = (math.sin(radians))
        
        # calculate change in x,y
        self.dx += (self.ddx * self.speed) * TIMESTEP
        self.dy += (self.ddy * self.speed) * TIMESTEP

        # update the rects
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # check for screen bounds, kill if offscreen
        if not self.bounds.contains(self.rect):
            self.kill()

class Explosion(engine.objects.AnimatedSprite):
    """ Explosion animation """
    def __init__(self, x, y, images):
        engine.objects.AnimatedSprite.__init__(self,x,y,images)
        self.hitbox = None

    def update(self, current_time):
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
    def __init__(self, game, x, y, images, angle):
        Bullet.__init__(self, game, x, y, images[0])
        self.images = images
        self.hitbox = pygame.Rect(self.dx,self.dy,6,6)
        self.hb_offsetx = 1
        self.hb_offsety = 1
        self.speed = 35
        self.diag_speed = self.speed / math.sqrt(2)
        self.angle = angle

    def update(self, current_time):

        # update dx, dy based on angle
        if self.angle == 0:
            self.image = self.images[4]
            self.dx += self.speed * TIMESTEP
        elif self.angle == 45:
            self.image = self.images[3]
            self.dx += self.diag_speed * TIMESTEP
            self.dy -= self.diag_speed * TIMESTEP
        elif self.angle == 90:
            self.image = self.images[2]
            self.dy -= self.speed * TIMESTEP
        elif self.angle == 135:
            self.image = self.images[1]
            self.dx -= self.diag_speed * TIMESTEP
            self.dy -= self.diag_speed * TIMESTEP
        elif self.angle == 180:
            self.image = self.images[0]
            self.dx -= self.speed * TIMESTEP
        elif self.angle == 225:
            self.image = self.images[7]
            self.dx -= self.diag_speed * TIMESTEP
            self.dy += self.diag_speed * TIMESTEP
        elif self.angle == 270:
            self.image = self.images[6]
            self.dy += self.speed * TIMESTEP
        elif self.angle == 315:
            self.image = self.images[5]
            self.dx += self.diag_speed * TIMESTEP
            self.dy += self.diag_speed * TIMESTEP

        # update the rects
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # check for screen bounds, kill if offscreen
        if not self.bounds.contains(self.rect):
            self.kill()
