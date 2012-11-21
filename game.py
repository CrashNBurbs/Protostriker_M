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

class PsmGame(engine.system.Game):

    def __init__(self):
        engine.system.Game.__init__(self)
        self.set_caption("Protostriker M")
        self.display.init()
        self.image_manager.load_font('prstartk.ttf', 8)
        self.font = self.image_manager.get_font()
        self.text_color = (252,248,252)
        self.push_state(states.TitleScreenState(self))

        
        
        
        





