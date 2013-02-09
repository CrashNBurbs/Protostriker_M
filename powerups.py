#-----------------------------------------------------------------------------
#  powerups.py
#  contains all the classes for different powerups
#-----------------------------------------------------------------------------

import pygame
from engine.system import TIMESTEP
from engine.system import SCREEN_RECT

class PowerUp(pygame.sprite.Sprite):
    """ PowerUp Class - A power up sprite that can be collected by 
        the player.  Power up types: 0 -  Spreader Gun, 1 - Reverse Fire Gun,
        2 - Laser Beam, 3 - Move Speed, 4 - Fire Speed """
    def __init__(self, game, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type 
        self.image = game.image_manager.get_image('powerups')[type]
        self.sound = game.sound_manager.get_sound('powerup')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = self.rect.x
        self.dy = self.rect.y
        self.speed = 50
        self.bounds = SCREEN_RECT
        self.hitbox = pygame.Rect(self.dx, self.dy, 14, 12)
        self.hb_offsetx = 1
        self.hb_offsety = 2
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

    def update(self, *args):
        self.dx -= self.speed * TIMESTEP

        self.rect.x = self.dx
        self.hitbox.x = self.rect.x + self.hb_offsetx

        if self.rect.left < self.bounds.left:
            self.kill()

    def collect(self):
        # returns an integer id for power up type
        self.sound.play()
        self.kill()
        return self.type

            