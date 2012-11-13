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

class StartMenu(engine.gui.Menu):
    """ Menu on titlescreen
    Options - START, OPTIONS, QUIT  """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)
        self.options_menu = OptionMenu(game, 52, 144, ['TOGGLE FULLSCREEN/WINDOW', 'CONTROLS', 'BACK'])

    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self, game)
        if selected == 'START':
            return True
        elif selected == 'OPTIONS':
            game.menu_manager.push_menu(self.options_menu)
        elif selected == 'QUIT':
            game.state_manager.quit()

class PauseMenu(engine.gui.Menu):
    """ First menu that displays on pause
    Options - RESUME, OPTIONS, QUIT TO TITLE, QUIT GAME """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)
        self.options_menu = OptionMenu(game, 52, 16, ['TOGGLE FULLSCREEN/WINDOW',
                                 'CONTROLS', 'BACK'])

    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self)
        if selected == 'RESUME':
            game.menu_manager.pop_menu(game.display.get_screen())
            game.state_manager.pop_state()
        elif selected == 'OPTIONS':
            game.menu_manager.push_menu(self.options_menu)
        elif selected == 'OUIT TO TITLE':
            game.menu_manager.pop_menu(game.display.get_screen())
            game.state_manager.pop_all()
        elif selected == 'QUIT GAME':
            game.state_manager.quit()


class OptionMenu(engine.gui.Menu):
    """ Options menu, nested in Pause menu
    Options - FULLSCREEN/WINDOW, CONTROLS, BACK """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)
        self.controls_menu = ControlsMenu(game, 84, 128, ['VIEW DEFAULT','RECONFIGURE',
                                'RESET TO DEFAULT','CHECK GAMEPAD', 'BACK'])

    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self, game)
        if selected == 'TOGGLE FULLSCREEN/WINDOW':
            game.display.change_mode()
        elif selected == 'CONTROLS':
            game.menu_manager.push_menu(self.controls_menu)
        elif selected == 'BACK':
            game.menu_manager.pop_menu(game.display.get_screen())

class ControlsMenu(engine.gui.Menu):
    """ Controls Menu, nested in options menu
    Options -  VIEW DEFAULT, RECONFIGURE
    RESET TO DEFAULT, CHECK GAMEPAD, BACK
    Shows various dialog boxes based on the option selected """
    def __init__(self, game, x, y, options):
        engine.gui.Menu.__init__(self, game, x, y, options)

        self.view_controls = engine.gui.DialogBox(game, 16, 160)
        self.view_controls.set_text(['MOVE - arrow keys or D-pad' \
                                    +'\nSHOOT\CONFIRM - Z key or button 2'])

        self.reset_dialog = engine.gui.DialogBox(game, 16, 160)
        self.reset_dialog.set_text(['Controls reset to default!'])
        self.config_screen = ConfigDialogBox(game, 16, 160)
        self.config_screen.set_text(['Press button for LEFT',
                                     'Press button for RIGHT',
                                     'Press button for UP',
                                     'Press button for DOWN',
                                     'Press button for SHOOT',
                                     'Press button for START',
                                     'Configure Complete!'])

        self.gamepad_dialog = engine.gui.DialogBox(game, 16, 160)

    def check_gamepad(self, input_manager):
        # Show gamepad name if gamepad is detected.
        # show error message if not.
        if input_manager.gamepad_name is not None:
            gamepad_text = self.game.input_manager.gamepad_name + '\nDetected'
        else:
            gamepad_text = 'Gamepad not detected\nPlease plug in a gamepad ' \
                                + 'and\nrestart the game'
        self.gamepad_dialog.set_text([gamepad_text])


    def handle_input(self, game):
        # call parent class handle input method, get
        # selected option, call appropriate methods
        selected = engine.gui.Menu.handle_input(self, game)
        if selected == 'VIEW DEFAULT':
            game.menu_manager.push_menu(self.view_controls)
        elif selected == 'RECONFIGURE':
            game.input_manager.toggle_config_mode()
            game.menu_manager.push_menu(self.config_screen)
        elif selected == 'RESET TO DEFAULT':
            game.menu_manager.push_menu(self.reset_dialog)
            game.input_manager.toggle_default()
        elif selected == 'CHECK GAMEPAD':
            self.check_gamepad(game.input_manager)
            game.menu_manager.push_menu(self.gamepad_dialog)
        elif selected == 'BACK':
            game.menu_manager.pop_menu(game.display.get_screen())

class ConfigDialogBox(engine.gui.DialogBox):
    """ Guides the user in setting a custom button config
    Each dialog box page will prompt the user to press a button
    they wish to assign to that control. """
    def __init__(self, game, x, y):
        engine.gui.DialogBox.__init__(self, game, x, y)
        # buttons to reconfigure
        self.buttons = ['LEFT', 'RIGHT', 'UP', 'DOWN',
                        'B','START']
        self.current = 0  # index of current button

    def handle_input(self, game):
        # Show each dialog box page, prompt user for a
        # button press, assign that button to a control.

        if self.page < 6:  # buttons left to configure
            if not self.page_done:  # only get button presses when the page is done
                pygame.event.clear()
            new_value = game.input_manager.config_process_input() # get input, assign to new_value
            new_value = game.input_manager.convert_dpad(new_value) # convert hat motion values to string
            if new_value is not None and new_value not in game.input_manager.set:  # if a key has been pressed
                if self.current <= len(self.buttons): # keep button index in bounds
                    # set current button to new value
                    game.input_manager.redefine_button(self.buttons[self.current], new_value)
                    self.current += 1  # move to next button
                self.progress()  # go to next page
        else:  # all buttons have been configured, showing 'config complete!'
            pressed = game.input_manager.config_process_input()  # get any key pressed
            if pressed:
                game.input_manager.toggle_user() # set input manager to check user buttons
                game.input_manager.toggle_config_mode() # go back to normal input handling
                self.current = 0 # reset index
                self.progress() # advance and close dialog box
