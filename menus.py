#-------------------------------------------------------------------------------
# Name:        Menus.py
# Purpose:     Contains the classes for all menus in the game
#
# Author:      Will Taplin
#
# Created:     02/12/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import pygame
import engine
import game
import states

class StartMenu(engine.gui.Menu):
    """ Menu on titlescreen
    Options - START, OPTIONS, QUIT  """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)

    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self, game)
        if selected == 'START':
            return True
        elif selected == 'OPTIONS':
            options = ['TOGGLE FULLSCREEN/WINDOW', 'CONTROLS', 'BACK']
            game.menu_manager.push_menu(OptionMenu(game, 52, 144, options))
        elif selected == 'QUIT':
            game.quit()

class PauseMenu(engine.gui.Menu):
    """ First menu that displays on pause
    Options - RESUME, OPTIONS, QUIT TO TITLE, QUIT GAME """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)

    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self, game)
        if selected == 'RESUME':
            game.input_manager.clear()
            game.menu_manager.pop_menu()
            game.pop_state()
        elif selected == 'OPTIONS':
            options = ['TOGGLE FULLSCREEN/WINDOW', 'CONTROLS', 'BACK']
            game.menu_manager.push_menu(OptionMenu(game, 52, 16, options))
        elif selected == 'OUIT TO TITLE':
            return True
        elif selected == 'QUIT GAME':
            game.quit()

class OptionMenu(engine.gui.Menu):
    """ Options menu, nested in Pause menu
    Options - FULLSCREEN/WINDOW, CONTROLS, BACK """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)
      
    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self, game)
        if selected == 'TOGGLE FULLSCREEN/WINDOW':
            game.display.change_mode()
        elif selected == 'CONTROLS':
            options = ['VIEW DEFAULT',
                       'RECONFIGURE',
                       'RESET TO DEFAULT',
                       'CHECK GAMEPAD',
                       'BACK']
            game.menu_manager.push_menu(ControlsMenu(game, 84, 128, options))
        elif selected == 'BACK':
            game.menu_manager.pop_menu()

class ControlsMenu(engine.gui.Menu):
    """ Controls Menu, nested in options menu
    Options -  VIEW DEFAULT, RECONFIGURE
    RESET TO DEFAULT, CHECK GAMEPAD, BACK
    Shows various dialog boxes based on the option selected """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)

    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self, game)
        if selected == 'VIEW DEFAULT':
            text = ['MOVE - arrow keys or D-pad\nSHOOT\CONFIRM' \
                    + '- Z key or button 2']
            game.menu_manager.push_menu(engine.gui \
                                              .DialogBox(game, 16, 160, text))
        elif selected == 'RECONFIGURE':
            game.input_manager.toggle_config_mode()
            text = ['Press button for LEFT',
                    'Press button for RIGHT',
                    'Press button for UP',
                    'Press button for DOWN',
                    'Press button for SHOOT',
                    'Press button for START',
                    'Configure Complete!']
            game.menu_manager.push_menu(ConfigDialogBox(game, 16, 160, text))
        elif selected == 'RESET TO DEFAULT':
            text = ['Controls reset to default!']
            game.menu_manager.push_menu(engine.gui.DialogBox(game, 16, 160, 
                                                             text))
            game.input_manager.toggle_default()
        elif selected == 'CHECK GAMEPAD':
            if game.input_manager.has_gamepad():
                text = [game.input_manager.gamepad_name + '\nDetected']
            else:
                text = ['Gamepad not detected\nPlease plug in a gamepad ' \
                       + 'and\nrestart the game']
            game.menu_manager.push_menu(engine.gui.DialogBox(game, 16, 160, 
                                                             text))
        elif selected == 'BACK':
            game.menu_manager.pop_menu()

class ConfigDialogBox(engine.gui.DialogBox):
    """ Guides the user in setting a custom button config
    Each dialog box page will prompt the user to press a button
    they wish to assign to that control. """
    def __init__(self, game, x, y, text):
        engine.gui.DialogBox.__init__(self, game, x, y, text)
        # buttons to reconfigure
        self.buttons = ['LEFT', 'RIGHT', 'UP', 'DOWN',
                        'B','START']
        self.current = 0  # index of current button

    def handle_input(self, game):
        # Show each dialog box page, prompt user for a
        # button press, assign that button to a control.

        # configure a new button for each control
        if self.page < len(self.buttons):
            # only get button presses when the page is done
            if not self.page_done:  
                pygame.event.clear()
            # get input, assign to new_value
            new_value = game.input_manager.config_process_input()
            # if a key has been pressed
            if new_value is not None:  
                # set current button to new value
                button_bound = game.input_manager \
                                   .redefine_button(self.buttons[self.current],
                                                     new_value)
                # if button reconfig was successful
                if button_bound:
                    self.current += 1  # move to next button
                    self.progress()  # go to next page
        else:  # all buttons have been configured, showing 'config complete!'
            # get any key pressed
            pressed = game.input_manager.config_process_input()
            if pressed:
                # set input manager to check user buttons
                game.input_manager.toggle_user() 
                # go back to normal input handling
                game.input_manager.toggle_config_mode() 
                # reset index
                self.current = 0 
                # advance and close dialog box
                done = self.progress() 
                if done: # user has pressed a button
                    game.menu_manager.pop_menu()
