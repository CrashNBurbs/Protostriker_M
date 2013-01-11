#-------------------------------------------------------------------------------
# Name:        Player.py
# Purpose:     Class for the player sprite
#
# Author:      Will Taplin
#
# Created:     30/11/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
import engine
import bullets
import weapons
from pygame.locals import *
from engine.system import TIMESTEP
from engine.system import SCREEN_RECT

class Player(engine.objects.AnimatedSprite):
    """ Class for the player, represented by a
        spaceship. Note: intermediate values for x,y coords
        are used(dx,dy) to assign floating point values to
        rect attributes """

    def __init__(self, game, x, y, images):
        engine.objects.AnimatedSprite.__init__(self,x,y,images, 20)
        self.game = game
        self.default_speed = 60
        self.speed = self.default_speed
        self.speed_increment = 20
        self.max_speed = 120
        self.direction = [0,0] # [x,y]
        self.bounds = SCREEN_RECT
        self.weapons = [weapons.BasicWeapon(game), weapons.Laser(game)]
        self.has_spreader = False
        self.has_reverse_fire = False
        self.has_laser = False
        self.current_weapon_index = 0
        self.current_weapon = self.weapons[self.current_weapon_index]
        self.changed_weapon_time = 0
        self.change_weapon_delay = 500
        self.hb_offsetx = 1 # x offset of hitbox from self.rect
        self.hb_offsety = 3 # y offset of hitbox from self.rect
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 28, 8) # rect for collsion
        self.lives = 3
        self.respawn_point = -20 # x coord for player respawn
        self.respawning = False
        self.protected = False
        self.score = 0
        self.explosion_sound = game.sound_manager.get_sound('pl_exp')
        self.change_weapon_sound = game.sound_manager.get_sound('changeweapon')

    def update(self, *args):
        current_time = args[0]

        # show correct frame
        self.image = self.images[self.frame]
        self.current_weapon = self.weapons[self.current_weapon_index]

        # if not respawing, move ship, check bounds
        if not self.respawning:
            # calc change in movement based on direction
            if self.direction[0] > 0: # right
                self.dx += self.speed * TIMESTEP
            elif self.direction[0] < 0: # left
                self.dx -= self.speed * TIMESTEP
            if self.direction[1] > 0: # down
                self.frame = 1 # change image
                self.dy += self.speed * TIMESTEP
            elif self.direction[1] < 0: # up
                self.frame = 2 # change image
                self.dy -= self.speed * TIMESTEP

            # if not moving up or down, reset image to frame 1.
            if self.direction[1] == 0:
                self.frame = 0

            # check bounds
            if self.dx <= self.bounds.left:
                self.dx = self.bounds.left
            elif self.dx + self.image.get_width() >= self.bounds.right:
                self.dx = self.bounds.right - self.image.get_width()
            if self.dy <= self.bounds.top:
                self.dy = self.bounds.top
            elif self.dy + self.image.get_height() >= self.bounds.bottom:
                self.dy = self.bounds.bottom - self.image.get_height()

        else: # self.respawning == True
            # move ship back onscreen and return
            # control to the player
            self.frame = 0
            self.dx += self.speed * TIMESTEP
            if self.dx >= 16:
                self.respawning = False

        # If player has lost a ship, disable collision detection
        # for self.protect_duration m/s
        if self.protected:
            # flash while protected.
            if current_time - self.last_update > self.delay:
                self.frame += 3
                if self.frame >= len(self.images):
                    self.frame = 0
                self.image = self.images[self.frame]
                self.last_update = current_time

            # turn off protection after self.protect_duration m/s.
            if pygame.time.get_ticks() - self.explode_time > self.protect_duration:
                self.protected = False

        # update the rect and hitbox
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

    def handle_input(self, game, current_time):
        # assume no shots fired
        shots = []

        # check input, set direction to appropriate values
        if not self.respawning: # disable input if respawning
            if game.input_manager.is_held('UP'):
                self.direction[1] = -1
            elif game.input_manager.is_held('DOWN'):
                self.direction[1] = 1
            else: # not moving up or down
                self.direction[1] = 0

            if game.input_manager.is_held('LEFT'):
                self.direction[0] = -1
            elif game.input_manager.is_held('RIGHT'):
                self.direction[0] = 1
            else: # not moving left or right
                self.direction[0] = 0

            # cycle through weapons on 'Y' button press
            if game.input_manager.is_pressed('Y'):
                if current_time - self.changed_weapon_time > self.change_weapon_delay:
                    self.current_weapon_index += 1
                    if self.current_weapon_index > len(self.weapons) - 1:
                        self.current_weapon_index = 0
                    if len(self.weapons) > 1:
                        self.change_weapon_sound.play()
                    self.changed_weapon_time = pygame.time.get_ticks()

            # shoot on 'B' button press
            if game.input_manager.is_held('B'):
                shots = self.current_weapon.fire(current_time, self.rect)
        # return shot list   
        return shots

    def power_up(self, powerup):
        if powerup == 0: # Spreader Gun
            if not self.has_spreader:
                self.weapons.insert(0, weapons.Spreader(self.game))
                self.has_spreader = True
                self.current_weapon_index = 0
        elif powerup == 1: # Reverse Fire Gun
            if not self.has_reverse_fire:
                self.weapons.insert(0, weapons.ReverseFire(self.game))
                self.has_reverse_fire = True
                self.current_weapon_index = 0
        elif powerup == 2: # Laser Beam
            if not self.has_laser:
                self.weapons.insert(0, weapons.Laser(self.game))
                self.has_laser = True
                self.current_weapon_index = 0
        elif powerup == 3: # Move Speed
            if self.speed < self.max_speed:
                self.speed += self.speed_increment
        elif powerup == 4:  # Fire Rate
            self.current_weapon.power_up()

    def reset_pos(self):
        # reset player pos to original pos
        self.direction = [0,0]
        self.dx = 16
        self.dy = 112

    def explode(self):
        # create explosion sprite
        ex = bullets.Explosion(self.rect.x, self.rect.y, 
                               self.game.image_manager.get_image('explosion'))

        # play sound
        self.explosion_sound.play()

        # set speed back to default
        # lose all weapons except the basic weapon
        # reset boolean flags for weapons
        self.speed = self.default_speed
        self.weapons = [weapons.BasicWeapon(self.game)]
        self.has_spreader = False
        self.has_reverse_fire = False
        self.has_laser = False
        self.current_weapon_index = 0

        # save time of death and set timer for protection
        self.explode_time = pygame.time.get_ticks()
        self.protect_duration = 2000

        # If lives remain, disable player input, hide the
        # ship offscreen, toggle protected and respawning.
        if self.lives > 0:
            self.protected = True
            self.respawning = True
            self.dx = -20 - self.image.get_width()
            self.dy = 112

        else: # no lives remain, kill ship sprite
            self.kill()
            self.hitbox.y = -10

        # return explosion sprite
        return ex

