#----------------------------------------------------------------------------
# Name:        States.py
# Purpose:     Contains all the game states. Update, draw, and
#              input handling routines.
#
# Author:      Will Taplin
#
# Created:     30/11/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#----------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
import engine
import player
import menus
import sprite_manager
import hud

from engine.system import SCREEN_RECT

class TitleScreenState(engine.system.State):
    def __init__(self, game):
        engine.system.State.__init__(self, game)
       
    def load_content(self):
        # load images
        self.game.image_manager.load_single('titlescreen.bmp', 'title')

    def unload_content(self):
        # unload everything not used by future states
        self.game.image_manager.unload_image('title')

    def activate(self, transition):
        engine.system.State.activate(self, transition)
        # Play music, Show the start menu
        self.load_content()
        self.background = self.game.image_manager.get_image('title')
        self.game \
            .menu_manager \
            .push_menu(menus.StartMenu(self.game, 120, 144, 
                                       ['START', 'OPTIONS', 'QUIT']))
        
    def handle_input(self):
        # pass input to current menu,
        # push gamestate if user selects START
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
            self.game.change_state(GameState(self.game),
                                   engine.graphics.FadeAnimation("in"))

    def draw(self, screen):
        # Draw background and all menus
        screen.blit(self.background, (0,0))
        self.game.menu_manager.draw(screen)

        if self.transitioning:
            self.transition.draw(screen)

class GameState(engine.system.State):
    def __init__(self, game):
        engine.system.State.__init__(self, game)
        self.sprite_manager = sprite_manager.SpriteManager()
        self.font = game.font
        self.text_color = game.text_color
        self.level = game.current_level
        self.game_over_triggered = False
        self.level_complete = False

    def load_content(self):
        # load images
        self.game.image_manager.load_single('background.bmp', 'background')

    def unload_content(self):
        self.game.image_manager.unload_image('background')

    def activate(self, transition):
        engine.system.State.activate(self, transition)

        # load all images and sounds for the state
        self.load_content()

        # Clear the input manager
        self.game.input_manager.clear()

        # load the level on state activation
        level_string = 'level_%d.txt' % self.level
        self.sprite_manager.load_level(self.game, level_string)

        # play music
        #self.game.sound_manager.play_music("gamemusic.wav")

        # create player, viewport, score and lives render, 
        # add player to sprite manager group
        self.player = self.game.player
        self.background = self.game.image_manager.get_image('background')
        self.viewport = engine.graphics.Viewport(self.game, self.background)
        self.sprite_manager.add_sprite(self.player, 'player_group')
        self.score_render = self.font.render("SCORE " + str(self.player.score),
                                             False, self.text_color)
        self.lives_render = self.font.render("LIVES " + str(self.player.lives),
                                             False, self.text_color)
        # toggle game.paused 
        self.game.paused = False

        level_string = "LEVEL %d" % self.level
        self.message = engine.gui.Message(self.game, level_string, 4000) 
        self.show_message = True

        self.hud = hud.GameHud(self.game, self.player, (0,0,0))

    def reactivate(self, transition):
        engine.system.State.reactivate(self, transition)
        self.game.paused = False
        self.game.sound_manager.music_control('unpause')

    def handle_input(self):
        # input passed to the player object
        # player.handle_input() returns a bullet sprite if req's are met,
        # none if not.
        bullets = self.player.handle_input(self.game, pygame.time.get_ticks())
        for bullet in bullets:
            self.sprite_manager.add_sprite(bullet, 'player_shots')

        # On start button press, push the pause state
        if self.game.input_manager.is_pressed('START'):
            self.game.push_state(PauseState(self.game))

    def update(self):
        engine.system.State.update(self)

        # scroll the background
        self.viewport.update()

        # update all sprites
        self.sprite_manager.update(pygame.time.get_ticks(), self.viewport,
                                   self.player.rect)

        self.hud.update(self.player, self.game)

        # check for all collsions, get player death
        player_die = self.sprite_manager.check_collisions(self.player)

        # Decrement lives on player death (This is not done in the player
        # class because colliding with two sprites at once can result in
        # multiple lives lost)
        if player_die:
            self.player.lives -= 1
            # if player has lost all lives, push a game over event state
            if self.player.lives == -1:
                text = "GAME OVER"
                state = engine.objects.EventState(self.game, text, 
                                                  "gameovermusic.wav",
                                                  GameState(self.game))
                self.game.reset_player()
                self.game.change_state(state)
        
        # If player has reached the end of the level, create a
        # level complete message, set game over to True.
        if self.viewport.level_pos > 10400:
            end = self.game.next_level()
            if not end:  # go to next level
                text = "LEVEL %d COMPLETE!" % self.level
                state = engine.objects.EventState(self.game, text, 
                                                  "levelwin.wav", 
                                                  GameState(self.game))
                self.game.player.reset_pos()
                self.game.change_state(state)
               
            else:  # show ending
                text = "GAME OVER"
                state = engine.objects.EventState(self.game, text, 
                                                  "gameovermusic.wav",
                                                  TitleScreenState(self.game))
                self.game.change_state(state)
           
    def draw(self, screen):
        # draw the background and all sprites
        self.viewport.draw(screen)
        self.sprite_manager.draw(screen)

        self.hud.draw(screen)

        # draw the score and player lives
        #screen.blit(self.score_render, (8,8))
        #screen.blit(self.lives_render, (256,8))

        if self.show_message:
            self.show_message = self.message.show(screen)

        if self.transitioning:
            self.transition.draw(screen)

          # uncomment this code to display all the sprites image rects
          # in green, and their hitboxes (collision region) in red
        #pygame.draw.rect(screen, (0,255,0), self.player.rect, 1)
        #pygame.draw.rect(screen, (255,0,0), self.player.hitbox, 1)

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
    def __init__(self, game):
        engine.system.State.__init__(self, game)
        self.pause_sound = game.sound_manager.get_sound('pause')

    def activate(self, transition):
        engine.system.State.activate(self, transition)

        # On pause state activate, pause music, play sound
        # and push the pause menu on the menu manager
        self.game.paused = True
        self.game.sound_manager.music_control('pause')
        self.pause_sound.play()
        self.game \
            .menu_manager \
            .push_menu(menus.PauseMenu(self.game, 96, 40, ['RESUME','OPTIONS',
                            'OUIT TO TITLE','QUIT GAME']))

    def handle_input(self):
        # get the current menu and pass input to it
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
        
        # user has quit to title
        if self.done_exiting:
            self.game.menu_manager.pop_menu()
            self.game.reset()

    def draw(self, screen):
        # draw all menus
        self.game.menu_manager.draw(screen)

        if self.transitioning:
            self.transition.draw(screen)


