#----------------------------------------------------------------------------
# Name:        Game.py
# Purpose:     instance of Game class
#
# Author:      Will Taplin
#
# Created:     30/11/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#----------------------------------------------------------------------------
#!/usr/bin/env python
import pygame
import engine
import states
import player
import hud

from engine.system import SCREEN_RECT

class PsmGame(engine.system.Game):

    def __init__(self):
        engine.system.Game.__init__(self)
        self.set_caption("Protostriker M")
        self.display.init()
        self.image_manager.load_font('prstartk.ttf', 8)
        self.font = self.image_manager.get_font()
        self.text_color = (252,248,252)
        self.load_content()
        pygame.display.set_icon(self.image_manager.get_image('icon'))
        self.current_level = 1
        self.boss_level = False
        self.boss_level_triggered = False
        self.hud = hud.GameHud(self, (320, 32), (0,0,0))
        self.game_world = pygame.rect.Rect(0, SCREEN_RECT.top + self.hud.height,
                                           320, SCREEN_RECT.height - self.hud.height)
        self.game_world_last_level = pygame.rect.Rect(0, 
                                                      SCREEN_RECT.top + self.hud.height + 32,
                                                      320,
                                                      SCREEN_RECT.height - self.hud.height - 64)
        self.game_world_boss_level = pygame.rect.Rect(16,SCREEN_RECT.top + self.hud.height + 16,
                                                      SCREEN_RECT.right - 32,
                                                      SCREEN_RECT.height - self.hud.height - 32)
        self.player = player.Player(self, 16, 112, 
                                    self.image_manager.get_image('ship'))
     
        self.push_state(states.TitleScreenState(self), 
                        engine.graphics.FadeAnimation("in"))

    def next_level(self):
        # change to a new level and return False if there are more levels
        # otherwise return true
        end_game = False
        if self.current_level < 6:
            self.current_level += 1
        else:
            end_game = True
        return end_game

    def reset_player(self):
        # create a new player, resetting all values
        self.player = player.Player(self, 16, 112,
                                    self.image_manager.get_image('ship'))

    def reset(self, caller):
        # reset the game back to original state
        self.current_level = 6
        self.boss_level = False
        self.boss_level_triggered = False
        self.reset_player()

        # If called from TitleScreenState, no need to push another
        if caller != 'TitleScreenState':
            self.change_state(states.TitleScreenState(self), 
                              engine.graphics.FadeAnimation("in"))

    def load_content(self):
        self.image_manager.load_single('icon.bmp', 'icon', -1)
        self.image_manager.load_sheet('textborder.bmp', 'textborder',
                                           8, 8, False)
        self.image_manager.load_single('menuarrow.bmp', 'cursor', -1)
        self.image_manager.load_single('dialogarrow.bmp', 'arrow', -1)
        self.image_manager.load_sheet('ship1.bmp','ship', 32, 16, 
                                           False, -1)
        self.image_manager.load_sheet('enemy1.bmp', 'enemy_01', 16, 16, 
                                           False, -1)
        self.image_manager.load_sheet('enemy2.bmp', 'enemy_02', 16, 16,
                                           False, -1)
        self.image_manager.load_sheet('enemy3.bmp', 'enemy_03', 24,16, 
                                           False, -1)
        self.image_manager.load_sheet('enemy4.bmp', 'enemy_04', 16,16, 
                                           False, -1)
        self.image_manager.load_sheet('enemy5.bmp', 'enemy_05', 32,32, 
                                           False, -1)
        self.image_manager.load_sheet('enemy6.bmp', 'enemy_06', 16,16,
                                           False, -1)
        self.image_manager.load_sheet('enemy7.bmp', 'enemy_07', 24,16, 
                                           False, -1)
        self.image_manager.load_sheet('enemy11.bmp', 'enemy_11', 16, 16,
                                      False, -1)
        self.image_manager.load_sheet('enemy12.bmp', 'enemy_12', 16, 16,
                                      False, -1)
        self.image_manager.load_sheet('enemy13.bmp', 'enemy_13', 16, 16,
                                      False, -1)
        self.image_manager.load_sheet('enemy14.bmp', 'enemy_14', 16, 16,
                                      False, -1)
        self.image_manager.load_sheet('enemy15.bmp', 'enemy_15', 16, 16,
                                      False, -1)
        self.image_manager.load_single('laser.bmp', 'pshot',
                                            (255,0,255))
        self.image_manager.load_single('enemyshot.bmp', 'eshot', -1)
        self.image_manager.load_single('spreadershot.bmp', 'spreadshot', -1)
        self.image_manager.load_sheet('explosion.bmp', 'explosion', 16,16, 
                                           False, -1)
        self.image_manager.load_sheet('shrapnel.bmp', 'shrapnel', 8,8,
                                           False, (255,0,255))
        self.image_manager.load_sheet('powerups.bmp', 'powerups', 16,16,
                                      False, -1)
        self.image_manager.load_sheet('hudbars.bmp', 'hudbars', 16,8,
                                      False, -1)
        self.image_manager.load_single('smallship.bmp', 'smallship', 
                                       (255,0,255))
        self.image_manager.load_sheet('boss.bmp', 'boss', 64, 96, False, -1)

        # load sounds
        self.sound_manager.load_sound('cursor.wav', 'cursor',
                                           volume = 0.2)
        self.sound_manager.load_sound('select.wav', 'select',
                                           volume = 0.2)
        self.sound_manager.load_sound('blip.wav', 'blip', volume = 0.1)
        self.sound_manager.load_sound('pause.wav', 'pause')
        self.sound_manager.load_sound('enemy_exp.wav','en_exp',
                                           volume = 0.4)
        self.sound_manager.load_sound('player_exp.wav', 'pl_exp',
                                           volume = 0.4)
        self.sound_manager.load_sound('laser.wav', 'laser',
                                           volume = 0.2)
        self.sound_manager.load_sound('hit.wav', 'hit',
                                           volume = 0.4)
        self.sound_manager.load_sound('spreader.wav', 'spreader',
                                      volume = 0.4)
        self.sound_manager.load_sound('laserbeam.wav', 'laserbeam',
                                      volume = 0.3)
        self.sound_manager.load_sound('powerup.wav', 'powerup', volume = 0.5)
        self.sound_manager.load_sound('changeweapon.wav', 'changeweapon',
                                      volume = 0.5)
        self.sound_manager.load_sound('nohit.wav', 'nohit', volume = 0.4)

        
        





