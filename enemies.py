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
        self.hitbox = [pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 15, 12)]
        self.has_powerup = has_powerup
        self.powerup_type = 3 # speed
        self.points = 120 # point value
        self.explosion_sound = game.sound_manager.get_sound('en_exp')
        self.hits = 0 # number of hits enemy takes, 0 is a one-shot kill
        self.hit_sound = game.sound_manager.get_sound('hit')
        
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
        self.hitbox[0].x = self.rect.x + self.hb_offsetx

    def spawn(self, current_time):
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
    
    def hit(self, damage):
        # decrement hits on hit, play hit sound
        self.hits -= damage
        self.hit_sound.play()
        self.image = self.flash_image
       
    def explode(self):
        # play sound
        self.explosion_sound.play()

        # create explosion sprite
        ex = []
        anim = bullets.Explosion(self.rect.x, self.rect.y,
                               self.game.image_manager.get_image('explosion'))
        ex.append(anim)
        
        # get a powerup
        powerup = self.drop_powerup()

        # die
        self.kill()

        return ex, powerup

    def get_flash_image(self):
        # create a white out image of sprite for hit animation
        flash_image = self.image.copy()

        for x in range(flash_image.get_width()):
            for y in range(flash_image.get_height()):
                # change all non-transparent pixels to white
                if flash_image.get_at((x,y)) != (255,0,255):
                    flash_image.set_at((x,y), (255,255,255))
        flash_image.convert()
      
        return flash_image

class Enemy2(Enemy1):
    """ Second enemy type, moves in a straight line
    at a slow speed and shoots """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.speed = 25
        self.bullet_image = game.image_manager.get_image('eshot')
        self.shoot_speed = 185 #150  # shooting delay
        self.last_shot = 0 # time of last shot
        self.volley_speed = 2000 # volley of shots delay
        self.last_volley = 0 # time of last volley
        self.shooting = False
        self.shots = 0 # shots fired
        self.start_shoot = 290 # x coord to being firing
        self.stop_shoot = 64 # x coord to cease firing
        self.points = 90
        self.powerup_type = 4 # gun power

    def update(self, *args):
        current_time = args[0]
        # call parent class update for frame
        # animation and movement
        Enemy1.update(self, current_time)

        # set shooting to true every self.volley_speed m/s
        # if enemy has passed the start shooting pos
        if current_time - self.last_volley > self.volley_speed and \
        self.dx < self.start_shoot and self.dx > self.stop_shoot:
            self.shooting = True
        else:
            shot = None

        # fire three shots per volley
        if self.shooting:
            shot = self.shoot(current_time)
            if self.shots == 3: # reset values
                self.last_volley = current_time
                self.shooting = False
                self.shots = 0

        # return the bullet sprite if shooting
        # or None if not shooting
        return shot

    def shoot(self, current_time):
        # fire a shot at current pos, every
        # self.shoot_speed m/s, keep track of shots fired
        if current_time - self.last_shot > self.shoot_speed:
            shot = bullets.EnemyBullet(self.rect.left,
                             self.rect.centery, 0, self.bullet_image)
            self.shots += 1
            self.last_shot = current_time
        else:
            shot = None
        return shot

class Enemy3(Enemy1):
    """ Third enemy type, moves in a sine wave
    pattern at a moderate speed """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images, 40)
        self.speed = 75
        self.angle = 0.0  # starting point for sin calc
        self.radius = 2.75 #2.0 # value to scale sin calc by
        self.dAngle = 5.0 #5.0 # change in angle(affects freq and amp)
        self.hb_offsetx = 4
        self.hb_offsety = 1
        self.hitbox = [pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 18, 13)]
        self.points = 175
        self.powerup_type = 0 # spreader

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
        self.hitbox[0].y = self.rect.y + self.hb_offsety

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
        self.hitbox = [pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 14, 14)]
        self.explosion_image = game.image_manager.get_image('shrapnel')
        self.points = 125

    def update(self, *args):
        current_time = args[0]
        engine.objects.AnimatedSprite.update(self, current_time)

        # smaller vertical bounds on the last level
        if self.game.current_level == 6:
            self.bounds = self.game.game_world_last_level

        shot = None

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
        self.hitbox[0].x = self.rect.x + self.hb_offsetx
        self.hitbox[0].y = self.rect.y + self.hb_offsety

        # shoot at a delay
        if self.dx > self.stop_shoot:
            shot = self.shoot(current_time)

        # return bullet sprite if shooting,
        # None if not shooting
        return shot

    def spawn(self, current_time):
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

        powerup = self.drop_powerup()

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
        self.hitbox = [pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 25, 21)]
        self.hits = 6
        self.explosion_image = game.image_manager.get_image('shrapnel')
        self.flash_image = self.get_flash_image()
        self.powerup_type = 2 # laser beam

    def update(self, *args):
        current_time = args[0]
        Enemy1.update(self, current_time)

        shot = None

        if self.dx > self.stop_shoot:
            shot = self.shoot(current_time)
        return shot

    def shoot(self, current_time):
        # fire a shot at current pos, every
        # self.shoot_speed m/s, keep track of shots fired
        if current_time - self.last_shot > self.shoot_speed:
            shot = bullets.EnemyBullet(self.rect.left + 2,
                             self.rect.centery + 5, 0, self.bullet_image)
            self.last_shot = current_time
        else:
            shot = None
        return shot

    def explode(self):
        ex = []
        # create explosion sprite

        for angle in range(0,360,45):
            ex.append(bullets.Shrapnel(self.rect.centerx, self.rect.centery,
                                       angle, self.explosion_image))

        # play sound
        self.explosion_sound.play()

        powerup = self.drop_powerup()

        # die
        self.kill()

        return ex, powerup

class Enemy6(Enemy3):
    """ Wide sine-wave enemy """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy3.__init__(self, game, x, y, has_powerup, images)
        self.dAngle = 3.5
        self.radius = 3.25
        self.points = 125
        self.speed = 70
        self.hits = 0
        self.flash_image = self.get_flash_image()


class Enemy7(Enemy1):
    """ Homing enemy """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.speed = 95
        self.vspeed = 45
        self.direction = 0
        self.hb_offsetx = 4
        self.hb_offsety = 1
        self.hitbox = [pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 18, 13)]
        self.changed_dir = False
        self.hits = 2
        self.flash_image = self.get_flash_image()

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
        self.hitbox[0].x = self.rect.x + self.hb_offsetx
        self.hitbox[0].y = self.rect.y + self.hb_offsety

class Enemy8(Enemy1):
    """ enemy 1 type that moves left to right """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.speed = 135

    
    def spawn(self, current_time):
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
        self.hitbox[0].x = self.rect.x + self.hb_offsetx

class Enemy9(Enemy3):
    """ sine wave enemy that moves left to right """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy3.__init__(self, game, x, y, has_powerup, images)
        self.speed = 55

    def spawn(self, current_time):
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
        self.hitbox[0].x = self.rect.x + self.hb_offsetx
        self.hitbox[0].y = self.rect.y + self.hb_offsety

class Enemy10(Enemy9):
    """ Wide sine wave enemy that moves left to right """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy9.__init__(self, game, x, y, has_powerup, images)
        self.dAngle = 3.5
        self.radius = 3.25
        self.points = 250
        self.speed = 65

class Enemy11(Enemy2):
    """ enemy that shoots single shots at the player """
    def __init__(self, game, x, y, has_powerup, images):
        Enemy2.__init__(self, game, x, y, has_powerup, images)
        self.speed = 40
        self.shoot_speed = 1250
        self.bullet_speed = 75
        self.points = 155
        self.hb_offsetx = 1
        self.hb_offsety = 1
        self.hitbox = [pygame.Rect(self.dx + self.hb_offsetx,
                                  self.dy + self.hb_offsety, 14, 14)]
        self.has_powerup = has_powerup
        self.powerup_type = 1 # reverse fire gun
        self.hits = 2
        self.flash_image = self.get_flash_image()

    def update(self, *args):
        current_time = args[0]
        player_rect = args[1]
        Enemy1.update(self, current_time)

        shot = None

        if self.dx > self.stop_shoot:
            shot = self.shoot(current_time, player_rect)
        return shot

    def shoot(self, current_time, player_rect):
        # fire a shot at current pos, every
        # self.shoot_speed m/s, keep track of shots fired
        if current_time - self.last_shot > self.shoot_speed:
            angle = math.atan2(player_rect.centery - self.rect.centery,
                               player_rect.centerx - self.rect.centerx)

            shot = bullets.EnemyBulletAngle(self.rect.left,
                             self.rect.centery, angle, self.bullet_speed,
                             self.bullet_image)
            self.last_shot = current_time
        else:
            shot = None
        return shot

class Enemy12(Enemy1):
    """ enemy that shifts up and down at intervals """

    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.fps = 15
        self.speed = 90
        self.v_speed = 80
        self.bullet_speed = 110
        self.last_shifted_pos = self.rect.y
        self.max_shift = 48
        self.shift_time = 1000
        self.last_shift = 0
        # shift down first if enemy in upper half of screen
        if self.rect.y < 120:
            self.shift_direction = 1
        else: # shift up first if enemy in lower half of screen
            self.shift_direction = -1
        self.points = 150

    def update(self, *args):
        current_time = args[0]
        Enemy1.update(self, current_time)

        # shift up and down at a delay
        if current_time - self.last_shift > self.shift_time:
            self.dy += (self.v_speed * self.shift_direction) * TIMESTEP
            # shift until self.max_shift distance has been reached
            if abs(self.dy - self.last_shifted_pos) > self.max_shift:
                # save new pos, reverse shift direction
                self.last_shifted_pos = self.rect.y
                self.shift_direction *= -1
                self.last_shift = current_time

        # update rect and hitbox
        self.rect.y = self.dy
        self.hitbox[0].y = self.rect.y + self.hb_offsety


    def spawn(self, current_time):
        Enemy1.spawn(self, current_time)

        # set last shift to at spawn time to 
        # avoid shifting imediately 
        self.last_shift = current_time

class Enemy13(Enemy11):
    """ enemy that shifts and shoots at player """

    def __init__(self, game, x, y, has_powerup, images):
        Enemy11.__init__(self, game, x, y, has_powerup, images)
        self.fps = 15
        self.speed = 40
        self.v_speed = 110
        self.last_shifted_pos = self.rect.y
        self.max_shift = 48
        self.shift_time = 800
        self.last_shift = 0
        # shift down first if enemy in upper half of screen
        if self.rect.y < 120:
            self.shift_direction = 1
        else: # shift up first if enemy in lower half of screen
            self.shift_direction = -1
        self.points = 185
        self.powerup_type = 4
        self.flash_image = self.get_flash_image()


    def update(self, *args):
        # get shots from Enemy11 type
        shot = Enemy11.update(self, *args)
        current_time = args[0]

        # shift up and down at a delay
        if current_time - self.last_shift > self.shift_time:
            self.dy += (self.v_speed * self.shift_direction) * TIMESTEP
            # shift until self.max_shift distance has been reached
            if abs(self.dy - self.last_shifted_pos) > self.max_shift:
                # save new pos, reverse shift direction
                self.last_shifted_pos = self.rect.y
                self.shift_direction *= -1
                self.last_shift = current_time
        
        # update rect and hitbox
        self.rect.y = self.dy
        self.hitbox[0].y = self.rect.y + self.hb_offsety

        # shoot at player
        return shot

    def spawn(self, current_time):
        Enemy1.spawn(self, current_time)

        # set last shift to at spawn time to 
        # avoid shifting imediately 
        self.last_shift = current_time

class Enemy14(Enemy12):
    """ left to right shifting enemy """

    def __init__(self, game, x, y, has_powerup, images):
        Enemy12.__init__(self, game, x, y, has_powerup, images)
        self.speed = 80

    def update(self, *args):
        current_time = args[0]
        engine.objects.AnimatedSprite.update(self, current_time)
        
        # shift up and down at a delay
        if current_time - self.last_shift > self.shift_time:
            self.dy += (self.v_speed * self.shift_direction) * TIMESTEP
            # shift until self.max_shift distance has been reached
            if abs(self.dy - self.last_shifted_pos) > self.max_shift:
                # save new pos, reverse shift direction
                self.last_shifted_pos = self.rect.y
                self.shift_direction *= -1
                self.last_shift = current_time

        # calculate change in x
        self.dx += self.speed * TIMESTEP

        # kill sprite if offscreen
        if self.dx > self.bounds.right:
            self.kill()
        
        # update the rect
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox[0].x = self.rect.x + self.hb_offsetx
        self.hitbox[0].y = self.rect.y + self.hb_offsety

    def spawn(self, current_time):
        self.dx = self.bounds.left - self.rect.width
        self.last_shift = current_time

class Enemy15(Enemy13):
    """ left to right shooting shifting enemy """

    def __init__(self, game, x, y, has_powerup, images):
        Enemy13.__init__(self, game, x, y, has_powerup, images)

    def update(self, *args):
        current_time = args[0]
        player_rect = args[1]
        engine.objects.AnimatedSprite.update(self, current_time)

        # get shots
        shot = self.shoot(current_time, player_rect)

        # shift up and down at a delay
        if current_time - self.last_shift > self.shift_time:
            self.dy += (self.v_speed * self.shift_direction) * TIMESTEP
            # shift until self.max_shift distance has been reached
            if abs(self.dy - self.last_shifted_pos) > self.max_shift:
                # save new pos, reverse shift direction
                self.last_shifted_pos = self.rect.y
                self.shift_direction *= -1
                self.last_shift = current_time

        # calculate change in x
        self.dx += self.speed * TIMESTEP

        # kill sprite if offscreen
        if self.dx > self.bounds.right:
            self.kill()
        
        # update rect and hitbox
        self.rect.x = self.dx
        self.rect.y = self.dy
        self.hitbox[0].x = self.rect.x + self.hb_offsetx
        self.hitbox[0].y = self.rect.y + self.hb_offsety

        # shoot at player
        return shot

    def spawn(self, current_time):
        self.dx = self.bounds.left - self.rect.width
        self.last_shift = current_time

class Boss(Enemy1):
    def __init__(self, game, x, y, has_powerup, images):
        Enemy1.__init__(self, game, x, y, has_powerup, images)
        self.x = x
        self.speed = 70
        self.bounds = game.game_world_boss_level
        self.direction = [0,-1]
        self.begin_time = 3000
        self.behavior_1 = True
        self.behavior_2 = False
        self.behavior_cycle = 0
        self.bullet_image = game.image_manager.get_image('eshot')
        self.explosion_image = game.image_manager.get_image('shrapnel')
        self.shoot_speed = 1100 # shooting delay
        self.last_shot = 8000 # time of last shot
        self.no_hitsound = game.sound_manager.get_sound('nohit')
        self.hits = 2
        self.flash_image = self.get_flash_image()
        # init offsets for hitboxs
        self.hb_offset1 = (10,10)
        self.hb_offset2 = (22,46)
        self.hb_offset3 = (7,52)
        self.hb_offset4 = (46,64)
        self.hb_offset5 = (33,4)
        self.hb_offset6 = (44,12)
        self.target_offset = (24,22)
        # create hitboxes
        self.collision_rect1 = pygame.rect.Rect(self.dx + self.hb_offset1[0],
                                                self.dy + self.hb_offset1[1],
                                                20, 9)
        self.collision_rect2 = pygame.rect.Rect(self.dx + self.hb_offset2[0],
                                                self.dy + self.hb_offset2[1],
                                                24, 17)
        self.collision_rect3 = pygame.rect.Rect(self.dx + self.hb_offset3[0],
                                                self.dy + self.hb_offset3[1],
                                                13, 36)
        self.collision_rect4 = pygame.rect.Rect(self.dx + self.hb_offset4[0],
                                                self.dy + self.hb_offset4[1],
                                                11, 30)
        self.collision_rect5 = pygame.rect.Rect(self.dx + self.hb_offset5[0],
                                                self.dy + self.hb_offset5[1],
                                                8, 37)
        self.collision_rect6 = pygame.rect.Rect(self.dx + self.hb_offset6[0],
                                                self.dy + self.hb_offset6[1],
                                                13, 30)
        self.target_rect = pygame.rect.Rect(self.dx + self.target_offset[0],
                                            self.dy + self.target_offset[1],
                                            7, 11)
        # add hitbox offsets to list for update
        self.offsets = [self.hb_offset1, self.hb_offset2, self.hb_offset3,
                        self.hb_offset4, self.hb_offset5, self.hb_offset6,
                        self.target_offset]
        # add hitboxes to a list for update and collision checking
        self.hitbox = [self.collision_rect1, self.collision_rect2,
                       self.collision_rect3, self.collision_rect4,
                       self.collision_rect5, self.collision_rect6,
                       self.target_rect]

    def spawn(self, current_time):
        self.dx = self.x
        self.spawn_time = current_time

    def update(self, *args):
        current_time = args[0]
        player_rect = args[1]
        engine.objects.AnimatedSprite.update(self, current_time)

        shot = None

        # delay action for self.begin_time m/s
        if current_time - self.spawn_time > self.begin_time:
            if self.direction[1] == -1: # moving up
                self.dy -= self.speed * TIMESTEP
                if self.dy <= self.bounds.top:
                    self.dy = self.bounds.top
                    # count top bounds collision as one behavior cycle
                    self.cycle_behavior()
                    # set new directions based on behavior
                    if self.behavior_1: # move down
                        self.direction[0] = 0
                        self.direction[1] = 1
                    elif self.behavior_2: # move left
                        self.direction[0] = -1
                        self.direction[1] = 0 
            elif self.direction[1] == 1: # moving down
                 self.dy += self.speed * TIMESTEP
                 if self.dy + self.image.get_height() >= self.bounds.bottom:
                    self.dy = self.bounds.bottom - self.image.get_height()
                    if self.behavior_1: # move up
                        self.direction[0] = 0
                        self.direction[1] = -1
                    elif self.behavior_2: # move right
                         self.direction[0] = 1
                         self.direction[1] = 0
            elif self.direction[0] == -1: # moving left
                self.dx -= self.speed * TIMESTEP
                if self.dx <= self.bounds.left:
                    self.dx = self.bounds.left
                    self.direction[0] = 0
                    self.direction[1] = 1 # move down
            elif self.direction[0] == 1: # moving right
                self.dx += self.speed * TIMESTEP
                if self.dx + self.image.get_width() >= self.bounds.right:
                    self.dx = self.bounds.right - self.image.get_width()
                    self.direction[0] = 0
                    self.direction[1] = -1 # move up

            shot = self.shoot(current_time, player_rect)
                    
        # update the rect and hitbox
        self.rect.x = self.dx
        self.rect.y = self.dy
        # loop through and update hitboxes
        for i in range(len(self.hitbox)):
            box = self.hitbox[i]
            offset = self.offsets[i]
            box.x = self.rect.x + offset[0]
            box.y = self.rect.y + offset[1]

        return shot

    def cycle_behavior(self):
        # update cycle counter
        self.behavior_cycle += 1

        # switch behaviors after 5 cycles
        if self.behavior_cycle == 5:
            self.behavior_cycle = 0
            if self.behavior_1:
                self.behavior_1 = False
                self.behavior_2 = True
            elif self.behavior_2:
                self.behavior_2 = False
                self.behavior_1 = True

    def shoot(self, current_time, player_rect):
        # fire a shot at current pos, every
        # self.shoot_speed m/s, keep track of shots fired
        if current_time - self.last_shot > self.shoot_speed:
            # shoot at the player for behavior 2
            if self.behavior_2:
                angle = math.atan2(player_rect.centery - self.rect.centery,
                                   player_rect.centerx - self.rect.centerx)
                shot = bullets.EnemyBulletAngle(self.rect.left + 16,
                             self.rect.centery - 22, angle, 75, self.bullet_image)
            # shoot straight for behavior 1
            elif self.behavior_1:
                shot = bullets.EnemyBullet(self.rect.left + 16,
                                    self.rect.centery - 22, 
                                    0, self.bullet_image)
            
            self.last_shot = current_time
        else:
            shot = None
        return shot

    def hit(self, damage):
        # decrement hits on hit, play hit sound
        # take damage on target hitbox hit
        if damage > 0:
            self.hits -= damage
            self.hit_sound.play()
            self.image = self.flash_image
        else: # did not hit target hitbox, no damage
            self.no_hitsound.play()

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
        powerup = self.drop_powerup()

        return ex, powerup



