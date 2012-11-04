#-------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:     Run this to begin the game.
#
# Author:      Will Taplin
#
# Created:     30/11/2011
# Copyright:   (c) Owner 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import game
import states

def main():
    game.init() # create managers, load all assets

    titlescreen = states.TitleScreenState() # create initial state

    game.state_manager.push_state(titlescreen) # push it
    game.state_manager.run() # run it

if __name__ == '__main__':
    main()

