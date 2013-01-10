#-------------------------------------------------------------------------------
# Name:        GUI
# Purpose:     Component of Engine, contains the the menu and dialog
#              classes and the menu manager
# Author:      Will Taplin
#
# Created:     20/07/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
import system

class TextBox():
    """ Abstract base class for displaying a bordered text box in game.
        Menus, dialog boxes, etc. """
    def __init__(self, game):
        # create font
        self.font = game.font
        self.text_color = game.text_color
        # load border images
        self.border_tiles= game.image_manager.get_image('textborder')

    def build_text_box(self):
        # This function blits all menu elements to the menu background

        # add border tiles based on the size of the menu
        # top left corner
        self.background.blit(self.border_tiles[0], (0,0))
        # bottom left corner
        self.background.blit(self.border_tiles[1], 
                             (0, self.background.get_height() - 8))
        # top right corner
        self.background.blit(self.border_tiles[2], 
                             (self.background.get_width() - 8, 0))
        # bottom right corner
        self.background.blit(self.border_tiles[3], 
                             (self.background.get_width() - 8, 
                             self.background.get_height() - 8))
        # tile horizontal border
        for i in range(1, self.background.get_width() / 8 - 1):
            self.background.blit(self.border_tiles[4], (i * 8, 0))
            self.background.blit(self.border_tiles[5], 
                                 (i * 8, self.background.get_height() - 8))
        # tile vertical border
        for i in range(1, self.background.get_height() / 8 - 1):
            self.background.blit(self.border_tiles[6], (0, i * 8))
            self.background.blit(self.border_tiles[7], 
                                 (self.background.get_width() - 8, i * 8))

    def draw(self):
        pass

    def handle_input(self):
        pass

class Menu(TextBox):
    """ Creates a new menu on the screen at x,y coords and automaticlly
    sizes depending on the number of options in the menu.  Inherit from
    this class to create specific menus and handle input
    options - a list of desired options in string form """
    def __init__(self, game, x, y,options):
        TextBox.__init__(self, game)
        self.options = options
        self.current_option = 0  # option currently selected
        # load cursor and set rect
        self.width = self.calc_width()
        self.height = self.calc_height()
        self.background = pygame.Surface((self.width, self.height)).convert()
        self.rect = self.background.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cursor = game.image_manager.get_image('cursor')
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.x = 8  # x is always 8
        self.cursor_rect.y = 8  # set cursor at first option
        # load sounds
        self.cursor_sound = game.sound_manager.get_sound('cursor')
        self.select_sound = game.sound_manager.get_sound('select')
        self.build_menu()


    def build_menu(self):
        # This function blits all menu elements to the menu background

        self.build_text_box()  # call TextBox function to create the background

        # add the options
        opt_pos = 8  # initial pixel pos for first option
        for option in self.options:
            render = self.font.render(option, False, self.text_color)
            self.background.blit(render, (16, opt_pos))
            opt_pos += 16 # leave a space between options
        
        # add the cursor
        self.background.blit(self.cursor, (8, self.cursor_rect.y))  

    def update(self, time):
        # menus do not need to update every cycle
        # changes handled by move cursor and draw functions
        # (has this function to avoid menu type checking when
        # menu manager updates)
        pass

    def draw(self, screen):
        # draws the menu to the screen
        self.background.blit(self.cursor, (8, self.cursor_rect.y))
        screen.blit(self.background, (self.rect.x, self.rect.y))
       
    def calc_width(self):
        # steps throught options, sets width to the
        # longest option + border
        width = 0
        for option in self.options:
            w = len(option) * 8
            if w > width:
                width = w
        width += 24
        return width

    def calc_height(self):
        # calculates height needed by adding the height of
        # options text, space for border, and a space between each option
        font_height = len(self.options) * 8
        border_height = 16
        space_height = (len(self.options) - 1) * 8
        return font_height + border_height + space_height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def move_cursor(self, direction):
        # play cursor sound
        self.cursor_sound.play()
        # move cursor down (1) and up (-1)
        # erase previous cursor pos
        self.background.fill((0,0,0), self.cursor_rect)  
        if direction == 1:   # down
            # increase the option index
            self.current_option += 1 
            # wrap to the top if went past last option
            if self.current_option > len(self.options) - 1:  
                self.current_option = 0
                self.cursor_rect.y = 8
            else:
                self.cursor_rect.y += 16
        if direction == -1:  # up
            # decrease the option index
            self.current_option -= 1 
            # wrap to the bottom if went past first option
            if self.current_option < 0: 
                self.current_option = len(self.options) - 1
                self.cursor_rect.y = self.background.get_height() - 16
            else:
                self.cursor_rect.y -= 16

    def get_selected_option(self):
        # option was selected, play sound
        self.select_sound.play()  
        # return option string at current index
        return self.options[self.current_option] 

    def handle_input(self, game):
        # moves cursor up and down
        # returns selected option on B or START button press
        if game.input_manager.is_pressed('DOWN'):
            self.move_cursor(1)
        elif game.input_manager.is_pressed('UP'):
            self.move_cursor(-1)
        elif game.input_manager.is_pressed('B') or \
             game.input_manager.is_pressed('START'):
                self.selected = self.get_selected_option()
                return self.selected

class DialogBox(TextBox):
    """ A class for displaying dialog or text in-game """
    def __init__(self, game, x, y, text):
        TextBox.__init__(self, game)
        self.width = 288  # w,h of dialog boxes are always 288x72
        self.height = 72
        self.background = pygame.Surface((self.width, self.height)).convert()
        self.rect = self.background.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delay = 20  # text display speed
        self.last_update = 0
        self.sound = game.sound_manager.get_sound('blip')
        self.arrow = game.image_manager.get_image('arrow')
        self.inner_rect = pygame.Rect(8,8,272,56)  # rect of dialog box - border
        self.text_x = 8  # initital pos to draw text, just inside border
        self.text_y = 8
        self.char = 0
        self.page_done = False # false when still blitting text
        self.build_text_box()
        self.render = None
        self.text = text
        self.page = 0
        self.pages = len(text)

    def progress(self):
        # called when input from the player is given
        # either goes to the next page, or pops the
        # dialog box

        #only allow if text is done blitting
        if self.page_done:  
            # erase inside the border
            self.background.fill((0,0,0), self.inner_rect)  
            # reset text blit coords
            self.text_x = 8  
            self.text_y = 8
            # reset character index
            self.char = 0  
            # if there are more pages
            if self.page < self.pages-1:
                # go to the next page
                self.page += 1  
            else:  # close the dialog box
                return True


    def update(self, current_time):
        # draws the text one page at a time and
        # one character at a time
        current_page = self.text[self.page]  # get the current page
        self.page_done = False
        if self.char < len(current_page):  # stay in bounds of the current string
            letter = current_page[self.char] # get the letter at index self.char
            if current_time - self.last_update > self.delay:
                # render letters at a delay, staying within the border
                # and wrapping to the next line when needed, or specified with '\n'
                if self.text_x > self.inner_rect.width or letter == '\n':
                    self.text_x = 8  # start at the left again
                    self.text_y += 8 # drop down to the next line
                if letter != '\n': # consume newline char
                    self.render = self.font.render(letter, False, self.text_color)
                    self.background.blit(self.render, (self.text_x, self.text_y))
                    self.text_x += 8  # next char position
                    self.sound.play()  # blip, blip, blip...
                self.char += 1  # next letter
                self.last_update = current_time
        else:  # self.char index >= len(current_page)
            if self.page < self.pages - 1:  # if there are more pages
                self.background.blit(self.arrow, (136, 56))  # show arrow
                self.page_done = True  # page is done, allow input
            else:  # this is the last page
                self.page_done = True # allow input

    def draw(self, screen):
        # draw the dialog box to the screen, in it's current state
        screen.blit(self.background, (self.rect.x, self.rect.y))

    def handle_input(self, game):
        # go to next page or close dialog box
        # on B button press
        if game.input_manager.is_pressed('B'):
            done = self.progress()
            if done:
                game.menu_manager.pop_menu()

class Message():
    """ Message class for creating centered text messages that
    display for an amount of time """
    def __init__(self, game, message, lifetime):
        self.message = message
        self.lifetime = lifetime
        self.created = pygame.time.get_ticks()
        self.render = game.font.render(self.message, False, game.text_color)
        self.x = (system.SCREEN_RECT.width - self.render.get_width()) / 2
        self.y = (system.SCREEN_RECT.height - self.render.get_height()) / 2

    def show(self, screen):
        # shows the message for the duration of self.lifetime
        # returns true when message is done
        showing = True
        current_time = pygame.time.get_ticks()
        if current_time - self.created < self.lifetime:
            screen.blit(self.render, (self.x, self.y))
        else: # lifetime has passed
            showing = False
        return showing

class MenuManager():
    """ Menu manager class is a stack for menu objects with the ability
    to draw all menus on the stack and erase them.push a menu onto the
    stack to draw it and make it the currentmenu, pop it to hide it and
    restore the current menu to the previous menu """
    def __init__(self):
        self.menus = []

    def push_menu(self, menu):
        # Adds a menu to the top of the stack
        self.menus.append(menu)

    def pop_menu(self):
        # remove a menu from the stack
        self.menus.pop()

    def draw(self, screen):
        # draw all menus in the stack
        for menu in self.menus:
            menu.draw(screen)

    def get_current_menu(self):
        # returns the menu at the top
        # of the stack
        return self.menus[-1]

    def has_menu(self):
        # returns true if there are any menus
        # on the stack
        if self.menus != []:
            return True
        else:
            return False

class HudElement():
    """ Bass class for HUD elements such as score, power bars, etc """

    def __init__(self, game, size, pos, color):
        self.pos = pos
        self.color = color
        self.background = pygame.Surface((size[0], size[1])).convert()
        self.background.fill(self.color)
        self.font = game.font
        self.text_color = game.text_color

    def update(self):
        self.background.fill(self.color)

    def draw(self):
        pass

class Hud(TextBox):
    """ Base class for in-game HUD """

    def __init__(self, game, player, color):
        TextBox.__init__(self, game)
        self.game = game
        self.elements = []
        self.player = player
        self.color = color
        self.background = pygame.Surface((320, 32)).convert()
        self.background.fill(self.color)
        self.build_text_box()
    
    def update(self, *args):
        for element in self.elements:
            element.update(*args)

    def draw(self, screen):
        
        for element in self.elements:
            self.background.blit(element.background, element.pos)

        screen.blit(self.background, (0,0))