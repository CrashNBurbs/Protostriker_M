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
    new_game = game.PsmGame()
    new_game.load_content()
    new_game.run()

if __name__ == '__main__':
    main()

