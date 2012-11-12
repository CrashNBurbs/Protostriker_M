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

class GameState(engine.system.State):
    def __init__(self, game):
        engine.system.State.__init__(self)
        self.player = player.Player(16,112, game.image_manager.get_image('ship'))
        self.background = game.image_manager.get_image('background')
        self.viewport = engine.graphics.Viewport(self.background, self.player)
        self.sprite_manager = sprite_manager.SpriteManager()
        self.sprite_manager.add_sprite(self.player, 'player_group')
        self.screen = game.display.get_screen()
        self.pause = PauseState(game)
        self.font = game.image_manager.get_font()
        self.text_color = (252,248,252)
        self.score_render = self.font.render("SCORE " + str(self.player.score),
                                             False, self.text_color)
        self.lives_render = self.font.render("LIVES " + str(self.player.lives),
                                             False, self.text_color)
        self.game_over = False

    def activate(self):
        # Clear the input manager
        game.input_manager.clear()

        # load the level on state activation
        self.sprite_manager.load_level('level_1.txt')

        # play music
        game.sound_manager.play_music("gamemusic.wav")

        # Create messages, add to message list
        self.level_message = engine.gui.Message(132,116, "LEVEL 1", 3000)
        self.get_ready = engine.gui.Message(120,124,"GET READY!", 3000)
        self.messages = [self.level_message, self.get_ready]

    def reactivate(self):
        game.sound_manager.music_control('unpause')


    def handle_input(self):
        # input passed to the player object
        # player.handle_input() returns a bullet sprite if req's are met,
        # none if not.
        for player in self.sprite_manager.sprites['player_group']:
            bullet = player.handle_input(pygame.time.get_ticks())
            if bullet is not None:
                self.sprite_manager.add_sprite(bullet, 'player_shots')

        # On start button press, push the pause state
        if game.input_manager.is_pressed('START'):
            game.state_manager.push_state(self.pause)

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
            message = engine.gui.Message(124,116, "GAME OVER", 4000)
            self.messages.append(message)
            self.game_over = True

        # If player has reached the end of the level, create a
        # level complete message, set game over to True.
        if self.viewport.level_pos > 10400:
            message = engine.gui.Message(92,116, "LEVEL 1 COMPLETE!", 4000)
            self.messages.append(message)
            self.game_over = True

        # update the score display
        self.score_render = self.font.render("SCORE " + str(self.player.score),
                                False, self.text_color)

        # update lives display if not game over
        # (not checking if game over results in -1 being displayed)
        if not self.game_over:
            self.lives_render = self.font.render("LIVES " + str(self.player.lives),
                                False, self.text_color)

    def draw(self):
        # draw the background and all sprites
        self.viewport.draw()
        self.sprite_manager.draw(self.screen)

        # draw the score and player lives
        self.screen.blit(self.score_render, (8,8))
        self.screen.blit(self.lives_render, (256,8))

        # show any messages, pop game state on
        # message done if self.game_over
        for message in self.messages:
            done = message.show(pygame.time.get_ticks())
            if done and not self.game_over:
                self.messages.remove(message)
            elif done and self.game_over:
                game.state_manager.pop_state()

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
        self.screen = game.display.get_screen()
        self.pause_menu = menus.PauseMenu(96, 16, ['RESUME','OPTIONS',
                            'OUIT TO TITLE','QUIT GAME'])
        self.pause_sound = game.sound_manager.get_sound('pause')

    def activate(self):
        # On pause state activate, pause music, play sound
        # and push the pause menu on the menu manager
        game.sound_manager.music_control('pause')
        self.pause_sound.play()
        game.menu_manager.push_menu(self.pause_menu)

    def reactivate(self):
        # re-show the pause menu
        game.menu_manager.push_menu(self.pause_menu)

    def handle_input(self):
        # get the current menu and pass input to it
        current_menu = game.menu_manager.get_current_menu()
        current_menu.handle_input()

    def update(self):
        # update menus only if there is one
        if game.menu_manager.has_menu():
            game.menu_manager.get_current_menu().update(pygame.time.get_ticks())

    def draw(self):
        # draw all menus
        game.menu_manager.draw()

class TitleScreenState(engine.system.State):
    def __init__(self):
        engine.system.State.__init__(self)
        self.screen = game.display.get_screen()
        self.background = game.image_manager.get_image('title')
        self.game_state = GameState()
        self.menu = menus.StartMenu(120, 144, ['START', 'OPTIONS', 'QUIT'])

    def activate(self):
        # Play music, Show the start menu
        game.menu_manager.push_menu(self.menu)

    def reactivate(self):
        # Re-show the start menu,
        # Create new game state to reset all values
        game.sound_manager.music_control('pause')
        game.menu_manager.push_menu(self.menu)
        self.game_state = GameState()

    def handle_input(self):
        # pass input to current menu,
        # push gamestate if user selects START
        current_menu = game.menu_manager.get_current_menu()
        start_game = current_menu.handle_input()
        if start_game:
            game.menu_manager.pop_menu()
            game.state_manager.push_state(self.game_state)

    def update(self):
        # update menus only if there is one
        if game.menu_manager.has_menu():
            game.menu_manager.get_current_menu().update(pygame.time.get_ticks())

    def draw(self):
        # Draw background and all menus
        self.screen.blit(self.background, (0,0))
        game.menu_manager.draw()


