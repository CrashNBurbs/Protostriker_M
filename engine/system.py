#-------------------------------------------------------------------------------
# Name:        System
# Purpose:     Component of Engine, contains the display class, input manager
#              state class, and state manager
# Author:      Will Taplin
#
# Created:     03/07/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame
from pygame.locals import *
import os
import game
import graphics
import sound
import gui

""" Some notes about Framerate Independent game Updates:
This engine uses framerate independent game updates at a fixed timestep.

The basic theory is:
Instead of throttling the game loop with clock.tick(value to throttle by), We
let the game run as fast as the machine can go, but only make calls to update
the game at a fixed timestep. In my case, every 1/60 second (60 fps). All
movement and/or physics values (speed,gravity, etc) are then multiplied by 1/60
second to make them based on time, rather than framerate.  For example, sprites
will now move in pixels per second, as opposed to pixels per frame.  This is
important because framerate can vary wildly when not being throttled by
clock.tick(). Basing movement and physics updates on time ensures that the game
does not run too fast on powerful machines or too slow on older machines.
The advantage to this method is that we can draw as fast the machine can go,
thus achieving much smoother looking animation.

The basic algorithm used to acheive this is:
Measure the time passed since the last game loop (in fractions of a second)
and add it to an accumulator. If the time passed is at least 1/60 second,
update the game.  Subtract 1/60 second from the accumulator and
check again, updating until the accumulator holds less than 1/60 second.
Factor the time leftover in the accumulator into the next check for game updates
This keeps things smoother than just checking if the last loop took at
least 1/60 second.  """

SCREEN_RECT = pygame.rect.Rect(0,0,320,240)

class Display():
    """ This class handles the initialization of pygame, the window,
        the drawing buffer.  It also handles fullscreen and window toggling
        and provides access to the the buffer in which to draw.
        Instantiate display object, and call init() to get started """
    def __init__(self):
        self.screen = None   # the actual display
        self.buffer = None  # graphics buffer
        self.res = (320,240)  # size of the game and graphics buffer
        self.window_scale = None  # scale for window size
        self.fullscreen = False
        self.desktop_h = None  # height of desktop, in pixels
        self.caption = None  # window caption

    def init(self):
        res = self.res

        # center for window mode
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        # save the desktop res before setting mode
        desktop_h = pygame.display.Info().current_h

        # calculate scale for window mode
        self.window_scale = desktop_h / res[1]

        # if scaled height is the same as desktop height, window will be cut
        # off and aspect ratio will be distorted, use one scale smaller
        #if res[1] * self.window_scale == desktop_h:
            #self.window_scale -= 1

        # display, sets resolution at 2 times the size of the game res
        #self.screen = pygame.display.set_mode((res[0] * 2, res[1] * 2),
                                               #pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((res[0] * self.window_scale,
                                               res[1] * self.window_scale))

        # create a buffer that is the same size as the game resolution
        self.buffer = pygame.Surface((SCREEN_RECT.width, SCREEN_RECT.height))
        pygame.mouse.set_visible(False)  # turn off the mouse pointer display

        self.update()

    def update(self):
        #updates the display
        # scales the game size buffer, draws it to the screen
        res = self.res
        window_scale = self.window_scale
        if self.fullscreen:  # scale settings for fullscreen
            scaled_buffer = pygame.transform.scale(self.buffer,
                                                  (res[0] * 2, res[1] * 2))
        else:  # scale settings for windowed mode
            scaled_buffer = pygame.transform.scale(self.buffer,
                                                   ((res[0] * window_scale,
                                                     res[1] * window_scale)))

        self.screen.blit(scaled_buffer, (0,0))
        pygame.display.flip()

    def change_mode(self):
        # toggles between fullscreen and windowed modes
        res = self.res
        window_scale = self.window_scale
        if self.fullscreen:
            pygame.display.set_caption(self.caption)
            self.screen = pygame.display.set_mode((res[0] * window_scale,
                                                   res[1] * window_scale))
            self.fullscreen = False
        else:
            self.screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
            self.fullscreen = True

    def get_screen(self):
        # get game size offscreen buffer, always draw to this surface
        return self.buffer

    def get_screen_bounds(self):
        # return the rect of the offscreen buffer
        return self.buffer.get_rect()

    def set_caption(self, caption):
        pygame.display.set_caption(caption)
        self.caption = caption


class InputManager():
    """ This class processes the pygame event queue and checks
        the bound 'buttons' for pressed and held states.
        call handle_input() every game loop to process input.
        is_pressed(button) and is_held(button) returns true if
        button is pressed or held, respectively """

    def __init__(self):
        pygame.joystick.init()
        self.redefined = False  # Start with default controls
        # dictionary of held buttons
        self.held = {'keys' : [], 'buttons' : [], 'dpad' : []}
         # dictionary of pressed buttons
        self.pressed = {'keys' : [], 'buttons' : [], 'dpad' : []}
        self.config_mode = False
        self.set = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        self.gamepad_name = None
        if pygame.joystick.get_count() > 0: # if gamepad plugged in
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            self.gamepad_name = self.gamepad.get_name()

        # bound controls
        # keys are of the SNES designation to take advantage of modern
        # gamepads, values are the pygame constants for the keyboard
        # pass keys to is_pressed, is_held check for button states
        self.default_bound = {'RIGHT': [K_RIGHT, 'right'],
                              'LEFT' : [K_LEFT, 'left'],
                              'UP' : [K_UP, 'up'],
                              'DOWN' : [K_DOWN, 'down'],
                              'SELECT' : [K_QUOTE, 8],
                              'START' : [K_RETURN, 9],
                              'B' : [K_z, 2],
                              'A' : [K_x, 1],
                              'Y' : [K_a, 3],
                              'X' : [K_s, 0]}

        self.user_bound = {'RIGHT' : [],  # separate dictionary for user
                           'LEFT' : [],   # bound controls
                           'UP' : [],
                           'DOWN' : [],
                           'SELECT' : [],
                           'START' : [],
                           'B' : [],
                           'A' : [],
                           'Y' : [],
                           'X' : []}

    def process_input(self):
        if not self.config_mode:
            #reset pressed buttons every call
            self.pressed = {'keys' : [], 'buttons' : [], 'dpad' : []}
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                # keypress event
                elif event.type == KEYDOWN:  
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        quit()
                    self.pressed['keys'].append(event.key)
                    self.held['keys'].append(event.key)
                # key release event
                elif event.type == KEYUP:   
                    if event.key in self.held['keys']:
                        self.held['keys'].remove(event.key)
                # gamepad button press event
                elif event.type == JOYBUTTONDOWN:
                    self.pressed['buttons'].append(event.button)
                    self.held['buttons'].append(event.button)
                # gamepad button release event
                elif event.type == JOYBUTTONUP:
                    if event.button in self.held['buttons']:
                        self.held['buttons'].remove(event.button)
                # d-pad
                elif event.type == JOYHATMOTION:  
                    dpad_state = []
                    if event.value[0] < 0:
                        dpad_state.append('left')
                    if event.value[0] > 0:
                        dpad_state.append('right')
                    if event.value[1] < 0:
                        dpad_state.append('down')
                    if event.value[1] > 0:
                        dpad_state.append('up')
                    self.update_dpad(dpad_state)
                    print self.held['dpad']

    def config_process_input(self):
        # input handling for control reconfiguration
        # checks for key/button down events and returns their value
        new_button = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                new_button = event.key
            elif event.type == JOYBUTTONDOWN:
                new_button = event.button
            elif event.type == JOYHATMOTION:
                if event.value[0] < 0:
                    new_button = 'left'
                if event.value[0] > 0:
                    new_button = 'right'
                if event.value[1] < 0:
                    new_button = 'down'
                if event.value[1] > 0:
                    new_button = 'up'
        return new_button

    def is_pressed(self, button):
        # returns true if button is pressed
        if self.redefined:  # if user has defined new controls
            if button in self.user_bound.iterkeys():
                values = self.user_bound[button]
        else:
            # if button is a bound button
            if button in self.default_bound.iterkeys():
                # get the list of bindings
                values = self.default_bound[button]

        # for each type (keyboard and gamepad)
        for key in self.pressed.iterkeys():
            # for each value in pressed
            for pressed in self.pressed[key]:
                # if pressed is found in the bindings
                if pressed in values:
                    return True
        # return false if the button passed in is not a bound button
        # or is not found in the list of pressed buttons
        return False

    def is_held(self, button):
        # returns true if a button is being held
        if self.redefined:
            if button in self.user_bound.iterkeys():
                values = self.user_bound[button]
        else:
            if button in self.default_bound.iterkeys():
                values = self.default_bound[button]

        for key in self.held.iterkeys():
            for held in self.held[key]:
                if held in values:
                    return True
        return False

    def update_dpad(self, state):
        # append string representations of gamepad hat (d-pad)
        # movements. can pass two strings in for diagonals
        self.held['dpad'] = []
        for button in state:
            self.pressed['dpad'].append(button)
            self.held['dpad'].append(button)

    def redefine_button(self, button, new_value):
        # adds new values to user made button configuration
        button_changed = False
        if new_value not in self.set:
            self.user_bound[button].append(new_value)
            self.set.append(new_value)
            button_changed = True
        return button_changed

    def toggle_default(self):
        # switch to default controls
        self.redefined = False

    def toggle_user(self):
        # switch to user defined controls
        self.redefined = True

    def toggle_config_mode(self):
        if self.config_mode == False:
            self.config_mode = True # switch to config event loop

            # reset bound buttons and block diagonal d-pad movements
            self.set = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

            # empty out all user bound controls
            self.user_bound =  {'RIGHT' : [],
                                'LEFT' : [],
                                'UP' : [],
                                'DOWN' : [],
                                'SELECT' : [],
                                'START' : [],
                                'B' : [],
                                'A' : [],
                                'Y' : [],
                                'X' : []}
        else: # returning from config mode
            self.config_mode = False

    def clear(self):
        # clear everything in input manager states
        # useful for state transitions
        self.held = {'keys' : [], 'buttons' : [], 'dpad' : []}
        self.pressed = {'keys' : [], 'buttons' : [], 'dpad' : []}

    def has_gamepad(self):
        # returns true if a gamepad is connected
        if self.gamepad_name is not None:
            return True

class State():
    """ Abstract state class, intended for inheritance
        handle_input, update, and draw all called every frame
        by the state manager """
    def __init__(self):
        pass

    def load_content(self):
        # load images and sounds for the state here
        pass

    def unload_content(self):
        # unload images and sounds that will not be used
        # again
        pass

    def activate(self):
        # called once when the state is first pushed
        # useful for starting music, sound effects, etc.
        pass

    def reactivate(self):
        # called once when a previous active state is
        # made active again.
        pass

    def handle_input(self):
        # All objects that process input should have their handle_input()
        # functions called here
        pass

    def update(self):
        # All objects that update should have their update() functions
        # called here
        pass

    def draw(self):
        # All objects that draw should have their draw() functions called
        # here
        pass




class Game():
    """ game class - Contains all managers, initializes pygame
        and runs a game loop """
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self.display = Display()
        self.image_manager = graphics.ImageManager()
        self.sound_manager = sound.SoundManager()
        self.menu_manager = gui.MenuManager()
        self.input_manager = InputManager()
        self.states = []
        self.initial_state = None
        self.clock = pygame.time.Clock()
        self.accumulator = 0.0
        self.timestep = 1 / 60.0

    def set_caption(self, caption):
        # set the window title bar to caption
        pygame.display.set_caption(caption)

    def load_content(self):
        # load all images and sounds here
        pass

    def get_current_state(self):
        return self.states[-1]

    def push_state(self, state):
        self.states.append(state)
        state.activate()

    def pop_state(self):
        self.states.pop()
        self.get_current_state().reactivate()

    def change_state(self, state):
        self.states.pop()
        self.states.append(state)
        state.activate()

    def pop_all(self):
        # This function will pop all states except the
        # first state pushed, which should be the title screen.
        for i in range(len(self.states) - 1):
            self.states.pop()
            self.get_current_state().reactivate()

    def run(self):
        current_state = self.get_current_state()
        while(current_state):
            # check for state change
            current_state = self.get_current_state()

            self.accumulator += self.clock.tick() / 1000.0

            self.input_manager.process_input()
            current_state.handle_input()

            while self.accumulator >= self.timestep:
                current_state.update()
                self.accumulator -= self.timestep
            
            for state in self.states:
                state.draw(self.display.get_screen())
            self.display.update()

    def quit(self):
        pygame.quit()
        quit()



