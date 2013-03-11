#-------------------------------------------------------------------------------
# Name:        Enemies.py
# Purpose:     Contains the classes from which are enemy types are
#              created.
#
# Author:      Will Taplin
#
# Created:     05/12/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import engine
import math
import pygame
import bullets
import random
import powerups
from engine.system import TIMESTEP
from engine.system import SCREEN_RECT

class Enemy1(engine.objects.AnimatedSprite):
    """ First enemy type, moves in a straight line
    at a high speed """
    def __init__(self, game, x, y, has_powerup, images, fps = 20):
        engine.objects.AnimatedSprite.__init__(self, x, y, images, fps)
        self.game = game
        self.speed = 145
        self.bounds = game.game_world
        self.hb_offsetx = 0 # offset for hitbox
        self.hb_offsety = 2
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 15, 12)
        self.has_powerup = has_powerup
        self.powerup_type = 3 # speed
        self.points = 160 # point value
        self.explosion_sound = game.sound_manager.get_sound('en_exp')
        self.hits = 0 # number of hits enemy takes, 0 is a one-shot kill
        

    def update(self, *args):
        current_time = args[0]

        # call parent class update function for frame
        # animation
        engine.objects.AnimatedSprite.update(self, current_time)

        # calculate change in x
        self.dx -= self.speed * TIMESTEP

        # kill sprite if offscreen
        if self.dx < self.bounds.left:
            self.kill()

        # update the rect
        self.rect.x = self.dx
        self.hitbox.x = self.rect.x + self.hb_offsetx

    def spawn(self):
        # Called when enemy should be onscreen.
        # Move enemy from its pos in the level
        # to the edge of the screen.
        self.dx = self.bounds.right

    def drop_powerup(self):
        # drop a speed powerup if self.has_powerup
        if self.has_powerup:
            powerup = powerups.PowerUp(self.game, self.rect.x, self.rect.y,
                                        self.powerup_type)
        else:
            powerup = None
        return powerup
       
    def explode(self):
        # play sound
        self.explosion_sound.play()

        # create explosion sprite
        ex = []
        anim = bullets.Explosion(self.rect.x, self.rect.y,
                               self.game.image_manager.get_image('explosion'))
        ex.append(anim)
        
        # die
        self.kill()

        # get a powerup
        powerup = self.drop_powerup()
        
        return ex, powerup

class Enemy2(Enemy1):
    """ Second enemy type, moves in a straight line
    at a slow speed and shoots """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.speed = 25
        self.bullet_image = game.image_manager.get_image('eshot')
        self.shoot_speed = 150  # shooting delay
        self.last_shot = 0 # time of last shot
        self.volley_speed = 2000 # volley of shots delay
        self.last_volley = 0 # time of last volley
        self.shooting = False
        self.shots = 0 # shots fired
        self.start_shoot = 290 # x coord to being firing
        self.points = 90
        self.powerup_type = 4

    def update(self, *args):
        current_time = args[0]
        # call parent class update for frame
        # animation and movement
        Enemy1.update(self, current_time)

        # set shooting to true every self.volley_speed m/s
        # if enemy has passed the start shooting pos
        if current_time - self.last_volley > self.volley_speed and \
        self.dx < self.start_shoot:
            self.shooting = True
        else:
            self.shot = None

        # fire three shots per volley
        if self.shooting:
            self.shoot(current_time)
            if self.shots == 3: # reset values
                self.last_volley = current_time
                self.shooting = False
                self.shots = 0

        # return the bullet sprite if shooting
        # or None if not shooting
        return self.shot

    def shoot(self, current_time):
        # fire a shot at current pos, every
        # self.shoot_speed m/s, keep track of shots fired
        if current_time - self.last_shot > self.shoot_speed:
            self.shot = bullets.EnemyBullet(self.rect.left,
                             self.rect.centery, 0, self.bullet_image)
            self.shots += 1
            self.last_shot = current_time
        else:
            self.shot = None

class Enemy3(Enemy1):
    """ Third enemy type, moves in a sine wave
    pattern at a moderate speed """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images, 40)
        self.speed = 95
        self.angle = 0.0  # starting point for sin calc
        self.radius = 2.0 # value to scale sin calc by
        self.dAngle = 5.0 # change in angle(affects freq and amp)
        self.hb_offsetx = 4
        self.hb_offsety = 1
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 18, 13)
        self.points = 210
        self.powerup_type = 0

    def update(self, *args):
        # call parent classes update method
        Enemy1.update(self, *args)

        # calculate change in y, sin of current angle
        # scaled by radius
        self.dy += math.sin(self.angle) * self.radius

        # increment the radius by dAngle, scaled by timestep
        self.angle += self.dAngle * TIMESTEP

        # update the rect
        self.rect.y = self.dy
        self.hitbox.y = self.rect.y + self.hb_offsety

class Enemy4(Enemy2):
    """ Fourth enemy type, moves into position and
    then vertical from the top to the bottom of the screen
    until destroyed """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy2.__init__(self, game, x, y, has_powerup, images)
        self.speed = 50
        self.direction = -1
        self.bounds = game.game_world
        self.shoot_speed = 1000
        self.spawn_point = 240 # x pos where enemy will be placed
        self.hb_offsetx = 1
        self.hb_offsety = 1
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 14, 14)
        self.explosion_image = game.image_manager.get_image('shrapnel')
        self.points = 125

    def update(self, *args):
        current_time = args[0]
        engine.objects.AnimatedSprite.update(self, current_time)

        # Move vertically on the screen, reversing direction
        # if screen bounds are hit
        if self.direction == -1: # moving up
            self.dy -= self.speed * TIMESTEP
            if self.dy <= self.bounds.top:
                self.dy = self.bounds.top
                self.direction = 1
        if self.direction == 1: # moving down
            self.dy += self.speed * TIMESTEP
            if self.dy + self.image.get_height() >= self.bounds.bottom:
                self.dy = self.bounds.bottom - self.image.get_height()
                self.direction = -1

        # update the rect
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

        # shoot at a delay
        self.shoot(current_time)

        # return bullet sprite if shooting,
        # None if not shooting
        return self.shot

    def spawn(self):
        # move sprite to self.spawn_point
        self.dx = self.spawn_point

    def explode(self):
        ex = []
        # create explosion sprite

        for angle in range(0,360,45):
            ex.append(bullets.Shrapnel(self.rect.centerx, self.rect.centery,
                                       angle, self.explosion_image))

        # play sound
        self.explosion_sound.play()

        # die
        self.kill()

        powerup = None

        return ex, powerup

class Enemy5(Enemy2):
    """ Large, multi-hit taking, enemy that creats shrapnel on explode """

    def __init__(self, game, x, y, has_powerup, images):
        Enemy2.__init__(self, game, x, y, has_powerup, images)
        self.speed = 15
        self.shoot_speed = 1000
        self.points = 250
        self.hb_offsetx = 4
        self.hb_offsety = 4
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 25, 21)
        self.hits = 4
        self.hit_sound = game.sound_manager.get_sound('hit')
        self.explosion_image = game.image_manager.get_image('shrapnel')

    def update(self, *args):
        current_time = args[0]
        Enemy1.update(self, current_time)

        self.shoot(current_time)
        return self.shot

    def shoot(self, current_time):
        # fire a shot at current pos, every
        # self.shoot_speed m/s, keep track of shots fired
        if current_time - self.last_shot > self.shoot_speed:
            self.shot = bullets.EnemyBullet(self.rect.left + 2,
                             self.rect.centery + 5, 0, self.bullet_image)
            self.last_shot = current_time
        else:
            self.shot = None

    def hit(self):
        # decrement hits on hit, play hit sound
        self.hits -= 1
        self.hit_sound.play()

    def explode(self):
        ex = []
        # create explosion sprite

        for angle in range(0,360,45):
            ex.append(bullets.Shrapnel(self.rect.centerx, self.rect.centery,
                                       angle, self.explosion_image))

        # play sound
        self.explosion_sound.play()

        # die
        self.kill()

        return ex

class Enemy6(Enemy3):
    """ Wide sine-wave enemy """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy3.__init__(self, game, x, y, has_powerup, images)
        self.dAngle = 3.5
        self.radius = 3.0
        self.points = 250
        self.speed = 75


class Enemy7(Enemy1):
    """ Homing enemy """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.speed = 95
        self.vspeed = 45
        self.direction = 0
        self.hb_offsetx = 4
        self.hb_offsety = 1
        self.hitbox = pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 18, 13)
        self.changed_dir = False

    def update(self, *args):
        current_time = args[0]
        player_rect = args[1]
        engine.objects.AnimatedSprite.update(self, current_time)

        if self.direction == 0:
            self.dx -= self.speed * TIMESTEP
        elif self.direction == 1:
            self.dy += self.vspeed * TIMESTEP
        elif self.direction == -1:
            self.dy -= self.vspeed * TIMESTEP

        if self.rect.x < player_rect.centerx and \
           self.rect.y < player_rect.y and\
           not self.changed_dir:
                self.direction = 1
                self.changed_dir = True
        elif self.rect.x < player_rect.centerx and \
             self.rect.y > player_rect.y and \
             not self.changed_dir:
                self.direction = -1
                self.changed_dir = True

        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

class Enemy8(Enemy1):
    """ enemy 1 type that moves left to right """
    def __init__(self, game, x, y, has_powerup, images):
        # Flip all images on their x axis
        # Call Enemy1 init, passing new flipped images
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.speed = 135

    
    def spawn(self):
        # Called when enemy should be onscreen.
        # Move enemy from its pos in the level
        # to the edge of the screen.
        self.dx = self.bounds.left - self.rect.width

    def update(self, *args):
        current_time = args[0]

        # call parent class update function for frame
        # animation
        engine.objects.AnimatedSprite.update(self, current_time)

        # calculate change in x
        self.dx += self.speed * TIMESTEP

        # kill sprite if offscreen
        if self.dx > self.bounds.right:
            self.kill()

        # update the rect
        self.rect.x = self.dx
        self.hitbox.x = self.rect.x + self.hb_offsetx

class Enemy9(Enemy3):
    """ sine wave enemy that moves left to right """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy3.__init__(self, game, x, y, has_powerup, images)
        self.speed = 85

    def spawn(self):
        # Called when enemy should be onscreen.
        # Move enemy from its pos in the level
        # to the edge of the screen.
        self.dx = self.bounds.left - self.rect.width

    def update(self, *args):
        current_time = args[0]
        engine.objects.AnimatedSprite.update(self, current_time)

        # calculate change in y, sin of current angle
        # scaled by radius
        self.dy += math.sin(self.angle) * self.radius
        self.dx += self.speed * TIMESTEP

        # increment the radius by dAngle, scaled by timestep
        self.angle += self.dAngle * TIMESTEP

        # kill sprite if offscreen
        if self.dx > self.bounds.right:
            self.kill()

        # update the rect
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox.x = self.rect.x + self.hb_offsetx
        self.hitbox.y = self.rect.y + self.hb_offsety

class Enemy10(Enemy9):
    """ Wide sine wave enemy that moves left to right """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy9.__init__(self, game, x, y, has_powerup, images)
        self.dAngle = 3.5
        self.radius = 3.0
        self.points = 250
        self.speed = 65