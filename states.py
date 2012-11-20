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
    def __init__(self, game):
        engine.system.State.__init__(self)
        self.game = game
        

    def load_content(self):
        # load images
        self.game.image_manager.load_single('titlescreen.bmp', 'title')
        self.game.image_manager.load_sheet('textborder.bmp', 'textborder', 8, 8, False)
        self.game.image_manager.load_single('menuarrow.bmp', 'cursor', -1)
        self.game.image_manager.load_single('dialogarrow.bmp', 'arrow', -1)

        # load sounds
        self.game.sound_manager.load_sound('pause.wav', 'pause')
        self.game.sound_manager.load_sound('cursor.wav', 'cursor', volume = 0.2)
        self.game.sound_manager.load_sound('select.wav', 'select', volume = 0.2)
        self.game.sound_manager.load_sound('blip.wav', 'blip', volume = 0.1)

    def activate(self):
        # Play music, Show the start menu
        self.load_content()
        self.background = self.game.image_manager.get_image('title')
        self.game \
            .menu_manager \
            .push_menu(menus.StartMenu(self.game, 120, 144, 
                                       ['START', 'OPTIONS', 'QUIT']))
                         
    def reactivate(self):
        # Re-show the start menu,                                             
        # Create new game state to reset all values
        self.game.sound_manager.music_control('pause')
        self.game \
            .menu_manager \
            .push_menu(menus.StartMenu(game, 120, 144, 
                                       ['START', 'OPTIONS', 'QUIT']))

    def handle_input(self):
        # pass input to current menu,
        # push gamestate if user selects START
        current_menu = self.game.menu_manager.get_current_menu()
        start_game = current_menu.handle_input(self.game)
        if start_game:
            self.game.menu_manager.pop_menu()
            self.game.change_state(GameState(self.game))

    def update(self):
        # update menus only if there is one
        if self.game.menu_manager.has_menu():
            self.game.menu_manager \
                .get_current_menu().update(pygame.time.get_ticks())

    def draw(self, screen):
        # Draw background and all menus
        screen.blit(self.background, (0,0))
        self.game.menu_manager.draw(screen)

class GameState(engine.system.State):
    def __init__(self, game):
        engine.system.State.__init__(self)
        self.game = game
        self.player = player.Player(game, 16, 112, 
                                    game.image_manager.get_image('ship'))
        self.background = game.image_manager.get_image('background')
        self.viewport = engine.graphics.Viewport(self.game, self.background)
        self.sprite_manager = sprite_manager.SpriteManager()
        self.sprite_manager.add_sprite(self.player, 'player_group')
        self.font = game.image_manager.get_font()
        self.text_color = (252,248,252)
        self.score_render = self.font.render("SCORE " + str(self.player.score),
                                             False, self.text_color)
        self.lives_render = self.font.render("LIVES " + str(self.player.lives),
                                             False, self.text_color)
        self.game_over = False

    def activate(self):
        # Clear the input manager
        self.game.input_manager.clear()

        # load the level on state activation
        self.sprite_manager.load_level(self.game, 'empty.txt')

        # play music
        self.game.sound_manager.play_music("gamemusic.wav")

        # Create messages, add to message list
        #self.level_message = engine.gui.Message(132,116, "LEVEL 1", 3000)
        #self.get_ready = engine.gui.Message(120,124,"GET READY!", 3000)
        #self.messages = [self.level_message, self.get_ready]

    def reactivate(self):
        self.game.sound_manager.music_control('unpause')


    def handle_input(self):
        # input passed to the player object
        # player.handle_input() returns a bullet sprite if req's are met,
        # none if not.
        for player in self.sprite_manager.sprites['player_group']:
            bullet = player.handle_input(self.game, pygame.time.get_ticks())
            if bullet is not None:
                self.sprite_manager.add_sprite(bullet, 'player_shots')

        # On start button press, push the pause state
        if self.game.input_manager.is_pressed('START'):
            self.game.paused = True
            self.game.push_state(PauseState(self.game))

    def update(self):
        # scroll the background
        self.viewport.update()

        # update all sprites
        self.sprite_manager.update(pygame.time.get_ticks(), self.viewport, self.player.rect)

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
            #message = engine.gui.Message(124,116, "GAME OVER", 4000)
            #self.messages.append(message)
            self.game_over = True

        # If player has reached the end of the level, create a
        # level complete message, set game over to True.
        if self.viewport.level_pos > 10400:
            #message = engine.gui.Message(92,116, "LEVEL 1 COMPLETE!", 4000)
            #self.messages.append(message)
            self.game_over = True

        # update the score display
        self.score_render = self.font.render("SCORE " + str(self.player.score),
                                False, self.text_color)

        # update lives display if not game over
        # (not checking if game over results in -1 being displayed)
        if not self.game_over:
            self.lives_render = self.font.render("LIVES " + str(self.player.lives),
                                False, self.text_color)

    def draw(self, screen):
        # draw the background and all sprites
        self.viewport.draw(screen)
        self.sprite_manager.draw(screen)

        # draw the score and player lives
        screen.blit(self.score_render, (8,8))
        screen.blit(self.lives_render, (256,8))

        # show any messages, pop game state on
        # message done if self.game_over
        #for message in self.messages:
        #    done = message.show(pygame.time.get_ticks())
        #    if done and not self.game_over:
        #        self.messages.remove(message)
        #    elif done and self.game_over:
        #        self.game.pop_state()

          # uncomment this code to display all the sprites image rects
          # in green, and their hitboxes (collision region) in red
##        pygame.draw.rect(self.screen, (0,255,0), self.player.rect, 1)
##        pygame.draw.rect(self.screen, (255,0,0), self.player.hitbox, 1)
##
##        for enemy in self.sprite_manager.sprites['enemy_group']:
##            pygame.draw.rect(self.screen, (0,255,0), enemy.rect, 1)
##            pygame.draw.rect(self.screen, (255,0,0), enemy.hitbox, 1)
##
##
##        for bullet in self.sprite_manager.sprites['player_shots']:
##            pygame.draw.rect(self.screen, (0,255,0), bullet.rect, 1)
##            pygame.draw.rect(self.screen, (255,0,0), bullet.hitbox, 1)
##
##        for shot in self.sprite_manager.sprites['enemy_shots']:
##            pygame.draw.rect(self.screen, (0,255,0), shot.rect, 1)
##            pygame.draw.rect(self.screen, (255,0,0), shot.hitbox, 1)

class PauseState(engine.system.State):
    """ pause menu state """
    def __init__(self, game):
        engine.system.State.__init__(self)
        self.game = game
        self.screen = game.display.get_screen()
        self.pause_sound = game.sound_manager.get_sound('pause')

    def activate(self):
        # On pause state activate, pause music, play sound
        # and push the pause menu on the menu manager
        self.game.sound_manager.music_control('pause')
        self.pause_sound.play()
        self.game \
            .menu_manager \
            .push_menu(menus.PauseMenu(self.game, 96, 16, ['RESUME','OPTIONS',
                            'OUIT TO TITLE','QUIT GAME']))

    def reactivate(self):
        # re-show the pause menu
        self.game \
            .menu_manager \
            .push_menu(menus.PauseMenu(self.game, 96, 16, ['RESUME','OPTIONS',
                            'OUIT TO TITLE','QUIT GAME']))

    def handle_input(self):
        # get the current menu and pass input to it
        current_menu = self.game.menu_manager.get_current_menu()
        current_menu.handle_input(self.game)

    def update(self):
        # update menus only if there is one
        if self.game.menu_manager.has_menu():
            self.game.menu_manager \
                .get_current_menu().update(pygame.time.get_ticks())

    def draw(self, screen):
        # draw all menus
        self.game.menu_manager.draw(screen)



