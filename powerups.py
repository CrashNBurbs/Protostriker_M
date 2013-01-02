#-----------------------------------------------------------------------------
#  powerups.py
#  contains all the classes for different powerups
#-----------------------------------------------------------------------------

import pygame
from engine.system import TIMESTEP
from engine.system import SCREEN_RECT

class PowerUp(pygame.sprite.Sprite):
    """ Base class for powerups """
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = self.rect.x
        self.dy = self.rect.y
        self.speed = 100
        self.bounds = SCREEN_RECT
        self.hitbox = pygame.Rect(self.dx, self.dy, 14, 12)
        self.hb_offsetx = 1
        self.hb_offsety = 2
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

    def update(self, *args):
        self.dx -= self.speed * TIMESTEP

        self.rect.x = dx
        self.hitbox.x = self.rect.x + self.hb_offsetx

        if self.rect.left < self.bounds.left:
            self.kill()