#-------------------------------------------------------------------------------
# Name:        States.py
# Purpose:     Contains all the game states. Update, draw, and
#              input handling routines.
#
# Author:      Will Taplin
#
# Created:     30/11/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
import engine
import player
import menus
import sprite_manager

class TitleScreenState(engine.system.State):
    def __init__(self, game, transition):
        engine.system.State.__init__(self, game, transition)
       
        
    def load_content(self):
        # load images
        self.game.image_manager.load_single('titlescreen.bmp', 'title')
        self.game.image_manager.load_sheet('textborder.bmp', 'textborder',
                                           8, 8, False)
        self.game.image_manager.load_single('menuarrow.bmp', 'cursor', -1)
        self.game.image_manager.load_single('dialogarrow.bmp', 'arrow', -1)

        # load sounds
        self.game.sound_manager.load_sound('pause.wav', 'pause')
        self.game.sound_manager.load_sound('cursor.wav', 'cursor',
                                           volume = 0.2)
        self.game.sound_manager.load_sound('select.wav', 'select',
                                           volume = 0.2)
        self.game.sound_manager.load_sound('blip.wav', 'blip', volume = 0.1)

    def unload_content(self):
        # unload everything not used by future states
        self.game.image_manager.unload_image('title')

    def activate(self):
        # Play music, Show the start menu
        self.load_content()
        self.background = self.game.image_manager.get_image('title')
        self.game \
            .menu_manager \
            .push_menu(menus.StartMenu(self.game, 120, 144, 
                                       ['START', 'OPTIONS', 'QUIT']))
        if self.transitioning:
            self.transition = engine.graphics.FadeAnimation("in")
                         
    def handle_input(self):
        # pass input to current menu,
        # push gamestate if user selects START
        if not self.transitioning:
            current_menu = self.game.menu_manager.get_current_menu()
            start_game = current_menu.handle_input(self.game)
            if start_game:
               self.transition_off(engine.graphics.FadeAnimation("out"))
            
    def update(self):
        engine.system.State.update(self)

        # update menus only if there is one
        if self.game.menu_manager.has_menu():
            self.game.menu_manager \
                .get_current_menu().update(pygame.time.get_ticks())

        if self.done_exiting:
            self.game.menu_manager.pop_menu()
            self.game.change_state(GameState(self.game, True))

    def draw(self, screen):
        # Draw background and all menus
        screen.blit(self.background, (0,0))
        self.game.menu_manager.draw(screen)

        if self.transitioning:
            self.transition.draw(screen)

class GameState(engine.system.State):
    def __init__(self, game, transition):
        engine.system.State.__init__(self, game, transition)
        self.sprite_manager = sprite_manager.SpriteManager()
        self.font = game.image_manager.get_font()
        self.text_color = (252,248,252)
        self.game_over = False

    def load_content(self):
        # load images
        self.game.image_manager.load_sheet('ship1.bmp','ship', 32, 16, 
                                           False, -1)
        self.game.image_manager.load_single('background.bmp', 'background')
        self.game.image_manager.load_sheet('enemy1.bmp', 'enemy1', 16, 16, 
                                           False, -1)
        self.game.image_manager.load_sheet('enemy2.bmp', 'enemy2', 16, 16,
                                           False, -1)
        self.game.image_manager.load_sheet('enemy3.bmp', 'enemy3', 24,16, 
                                           False, -1)
        self.game.image_manager.load_sheet('enemy4.bmp', 'enemy4', 16,16, 
                                           False, -1)
        self.game.image_manager.load_sheet('enemy5.bmp', 'enemy5', 32,32, 
                                           False, -1)
        self.game.image_manager.load_sheet('enemy6.bmp', 'enemy6', 16,16,
                                           False, -1)
        self.game.image_manager.load_sheet('enemy7.bmp', 'enemy7', 24,16, 
                                           False, -1)
        self.game.image_manager.load_single('playershot.bmp', 'pshot',
                                            (255,0,255))
        self.game.image_manager.load_single('enemyshot.bmp', 'eshot', -1)
        self.game.image_manager.load_sheet('explosion.bmp', 'explosion', 16,16, 
                                           False, -1)
        self.game.image_manager.load_sheet('shrapnel.bmp', 'shrapnel', 8,8,
                                           False, -1)

        # load sounds
        self.game.sound_manager.load_sound('enemy_exp.wav','en_exp',
                                           volume = 0.4)
        self.game.sound_manager.load_sound('player_exp.wav', 'pl_exp',
                                           volume = 0.4)
        self.game.sound_manager.load_sound('laser.wav', 'laser',
                                           volume = 0.2)
        self.game.sound_manager.load_sound('hit.wav', 'hit',
                                           volume = 0.4)
    def unload_content(self):
        # unload everything not used by future states
        for key in self.game.image_manager.images.keys():
            self.game.image_manager.unload_image(key)

        for key in self.game.sound_manager.sounds.keys():
            self.game.sound_manager.unload_sound(key)

    def activate(self):

        # load all images and sounds for the state
        self.load_content()

        # Clear the input manager
        self.game.input_manager.clear()

        # load the level on state activation
        self.sprite_manager.load_level(self.game, 'level_1.txt')

        # play music
        #self.game.sound_manager.play_music("gamemusic.wav")

        # create player, viewport, score and lives render, 
        # add player to sprite manager group
        self.player = player.Player(self.game, 16, 112, 
                                    self.game.image_manager.get_image('ship'))
        self.background = self.game.image_manager.get_image('background')
        self.viewport = engine.graphics.Viewport(self.game, self.background)
        self.sprite_manager.add_sprite(self.player, 'player_group')
        self.score_render = self.font.render("SCORE " + str(self.player.score),
                                             False, self.text_color)
        self.lives_render = self.font.render("LIVES " + str(self.player.lives),
                                             False, self.text_color)
        # toggle game.paused 
        self.game.paused = False

        if self.transitioning:
            self.transition = engine.graphics.FadeAnimation("in")

        self.message = engine.gui.Message(self.game, "LEVEL 1", 4000)
        self.show_message = True


    def reactivate(self):
        self.game.paused = False
        self.game.sound_manager.music_control('unpause')


    def handle_input(self):
        # input passed to the player object
        # player.handle_input() returns a bullet sprite if req's are met,
        # none if not.
        if not self.transitioning:
            for player in self.sprite_manager.sprites['player_group']:
                bullet = player.handle_input(self.game, pygame.time.get_ticks())
                if bullet is not None:
                    self.sprite_manager.add_sprite(bullet, 'player_shots')

            # On start button press, push the pause state
            if self.game.input_manager.is_pressed('START'):
                self.game.push_state(PauseState(self.game, False))

    def update(self):
        engine.system.State.update(self)

        # scroll the background
        self.viewport.update()

        # update all sprites
        self.sprite_manager.update(pygame.time.get_ticks(), self.viewport,
                                   self.player.rect)

        # check for all collsions, get player death
        player_die = self.sprite_manager.check_collisions(self.player)

        # Decrement lives on player death (This is not done in the player
        # class because colliding with two sprites at once can result in
        # multiple lives lost)
        if player_die:
            self.player.lives -= 1

        # if player has lost all lives, create a game over message,
        # set game over to True.
        if self.player.lives == -1:
            self.game_over = True

        # If player has reached the end of the level, create a
        # level complete message, set game over to True.
        if self.viewport.level_pos > 10400:
            self.game_over = True

        # update the score display
        self.score_render = self.font.render("SCORE " + str(self.player.score),
                                False, self.text_color)

        # update lives display if not game over
        # (not checking if game over results in -1 being displayed)
        if not self.game_over:
            self.lives_render = self.font.render("LIVES " + 
                                                 str(self.player.lives),
                                                 False, self.text_color)

    def draw(self, screen):
        # draw the background and all sprites
        self.viewport.draw(screen)
        self.sprite_manager.draw(screen)

        # draw the score and player lives
        screen.blit(self.score_render, (8,8))
        screen.blit(self.lives_render, (256,8))

        if self.show_message:
            self.show_message = self.message.show(screen)

        if self.transitioning:
            self.transition.draw(screen)

          # uncomment this code to display all the sprites image rects
          # in green, and their hitboxes (collision region) in red
        pygame.draw.rect(screen, (0,255,0), self.player.rect, 1)
        pygame.draw.rect(screen, (255,0,0), self.player.hitbox, 1)

        #for enemy in self.sprite_manager.sprites['enemy_group']:
        #    pygame.draw.rect(screen, (0,255,0), enemy.rect, 1)
        #    pygame.draw.rect(screen, (255,0,0), enemy.hitbox, 1)


        #for bullet in self.sprite_manager.sprites['player_shots']:
        #    pygame.draw.rect(screen, (0,255,0), bullet.rect, 1)
        #    pygame.draw.rect(screen, (255,0,0), bullet.hitbox, 1)

        #for shot in self.sprite_manager.sprites['enemy_shots']:
        #    pygame.draw.rect(screen, (0,255,0), shot.rect, 1)
        #    pygame.draw.rect(screen, (255,0,0), shot.hitbox, 1)

class PauseState(engine.system.State):
    """ pause menu state """
    def __init__(self, game, transition):
        engine.system.State.__init__(self, game, transition)
        self.pause_sound = game.sound_manager.get_sound('pause')

    def activate(self):
        # On pause state activate, pause music, play sound
        # and push the pause menu on the menu manager
        self.game.paused = True
        self.game.sound_manager.music_control('pause')
        self.pause_sound.play()
        self.game \
            .menu_manager \
            .push_menu(menus.PauseMenu(self.game, 96, 16, ['RESUME','OPTIONS',
                            'OUIT TO TITLE','QUIT GAME']))

    def handle_input(self):
        # get the current menu and pass input to it
        if not self.transitioning:
            current_menu = self.game.menu_manager.get_current_menu()
            reset_game = current_menu.handle_input(self.game)
            if reset_game:
                self.transition_off(engine.graphics.FadeAnimation("out"))

    def update(self):
        engine.system.State.update(self)

        # update menus only if there is one
        if self.game.menu_manager.has_menu():
            self.game.menu_manager \
                .get_current_menu().update(pygame.time.get_ticks())

        if self.done_exiting:
            self.game.menu_manager.pop_menu()
            self.game.change_state(TitleScreenState(self.game, True))

    def draw(self, screen):
        # draw all menus
        self.game.menu_manager.draw(screen)

        if self.transitioning:
            self.transition.draw(screen)

class Level1Transition(engine.graphics.Transition):
    def __init__(self, game, text):
        engine.graphics.Transition.__init__(self, game, text)

    def update(self):
        engine.graphics.Transition.update(self)

        if self.done:
            self.game.change_state(GameState(self.game))
