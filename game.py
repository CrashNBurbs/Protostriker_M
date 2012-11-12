#-------------------------------------------------------------------------------
# Name:        Game.py
# Purpose:     Create all game managers and provide a global
#              point of access to them. Load assets
#
# Author:      Will Taplin
#
# Created:     30/11/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import engine
import states

display = None
state_manager = None
image_manager = None
sound_manager = None
input_manager = None
menu_manager = None

def init():
    global display
    global state_manager
    global image_manager
    global sound_manager
    global input_manager
    global menu_manager

    # create and init the display
    display = engine.system.Display()
    display.init()
    display.set_caption("8-Bit Shooter")

    # create the image manager and load image assets
    image_manager = engine.graphics.ImageManager()
    image_manager.load_single('titlescreen.bmp', 'title')
    image_manager.load_sheet('ship1.bmp','ship', 32, 16, False, -1)
    image_manager.load_single('background.bmp', 'background')
    image_manager.load_sheet('textborder.bmp', 'textborder', 8, 8, False)
    image_manager.load_single('menuarrow.bmp', 'cursor', -1)
    image_manager.load_single('dialogarrow.bmp', 'arrow', -1)
    image_manager.load_sheet('enemy1.bmp', 'enemy1', 16, 16, False, -1)
    image_manager.load_sheet('enemy2.bmp', 'enemy2', 16, 16, False, -1)
    image_manager.load_sheet('enemy3.bmp', 'enemy3', 24,16, False, -1)
    image_manager.load_sheet('enemy4.bmp', 'enemy4', 16,16, False, -1)
    image_manager.load_sheet('enemy5.bmp', 'enemy5', 32,32, False, -1)
    image_manager.load_sheet('enemy6.bmp', 'enemy6', 16,16, False, -1)
    image_manager.load_sheet('enemy7.bmp', 'enemy7', 24,16, False, -1)
    image_manager.load_single('playershot.bmp', 'pshot', (255,0,255))
    image_manager.load_single('enemyshot.bmp', 'eshot', -1)
    image_manager.load_sheet('explosion.bmp', 'explosion', 16,16, False, -1)
    image_manager.load_sheet('shrapnel.bmp', 'shrapnel', 8,8, False, -1)

    # create the sound manager and load sound assets
    sound_manager = engine.sound.SoundManager()
    sound_manager.load_sound('pause.wav', 'pause')
    sound_manager.load_sound('cursor.wav', 'cursor', volume = 0.2)
    sound_manager.load_sound('select.wav', 'select', volume = 0.2)
    sound_manager.load_sound('blip.wav', 'blip', volume = 0.1)
    sound_manager.load_sound('enemy_exp.wav','en_exp', volume = 0.4)
    sound_manager.load_sound('player_exp.wav', 'pl_exp', volume = 0.4)
    sound_manager.load_sound('laser.wav', 'laser', volume = 0.2)
    sound_manager.load_sound('hit.wav', 'hit', volume = 0.4)

    # create non resource managers
    input_manager = engine.system.InputManager()
    state_manager = engine.system.StateManager()
    menu_manager = engine.gui.MenuManager()


class PsmGame(engine.system.Game):

    def __init__(self):
        engine.system.Game.__init__(self)
        self.initial_state = states.GameState(self)

    def load_content(self):
        # load images
        image_manager.load_single('titlescreen.bmp', 'title')
        image_manager.load_sheet('ship1.bmp','ship', 32, 16, False, -1)
        image_manager.load_single('background.bmp', 'background')
        image_manager.load_sheet('textborder.bmp', 'textborder', 8, 8, False)
        image_manager.load_single('menuarrow.bmp', 'cursor', -1)
        image_manager.load_single('dialogarrow.bmp', 'arrow', -1)
        image_manager.load_sheet('enemy1.bmp', 'enemy1', 16, 16, False, -1)
        image_manager.load_sheet('enemy2.bmp', 'enemy2', 16, 16, False, -1)
        image_manager.load_sheet('enemy3.bmp', 'enemy3', 24,16, False, -1)
        image_manager.load_sheet('enemy4.bmp', 'enemy4', 16,16, False, -1)
        image_manager.load_sheet('enemy5.bmp', 'enemy5', 32,32, False, -1)
        image_manager.load_sheet('enemy6.bmp', 'enemy6', 16,16, False, -1)
        image_manager.load_sheet('enemy7.bmp', 'enemy7', 24,16, False, -1)
        image_manager.load_single('playershot.bmp', 'pshot', (255,0,255))
        image_manager.load_single('enemyshot.bmp', 'eshot', -1)
        image_manager.load_sheet('explosion.bmp', 'explosion', 16,16, False, -1)
        image_manager.load_sheet('shrapnel.bmp', 'shrapnel', 8,8, False, -1)

        # load sounds and music
        sound_manager = engine.sound.SoundManager()
        sound_manager.load_sound('pause.wav', 'pause')
        sound_manager.load_sound('cursor.wav', 'cursor', volume = 0.2)
        sound_manager.load_sound('select.wav', 'select', volume = 0.2)
        sound_manager.load_sound('blip.wav', 'blip', volume = 0.1)
        sound_manager.load_sound('enemy_exp.wav','en_exp', volume = 0.4)
        sound_manager.load_sound('player_exp.wav', 'pl_exp', volume = 0.4)
        sound_manager.load_sound('laser.wav', 'laser', volume = 0.2)
        sound_manager.load_sound('hit.wav', 'hit', volume = 0.4)






