#-----------------------------------------------------------------------------
#  hud.py
#  contains all the classes for HUD elements and the HUD itself
#-----------------------------------------------------------------------------

import engine

class GameHud(engine.gui.Hud):

    def __init__(self, game, player):
        engine.gui.Hud.__init__(self, game, player)
        score = ScoreElement(game, (96,8), (0,4))
        gun = WeaponNameElement(game, (88,8), (110,4))
        self.elements.append(score)
        self.elements.append(gun)

class ScoreElement(engine.gui.HudElement):
    """ Player score """

    def __init__(self, game, size, pos):
        engine.gui.HudElement.__init__(self, game, size, pos)
        
    def update(self, player):
        self.background.fill((0,0,0))

        if player.score < 10:
            zeros = "00000"
        elif player.score < 100:
            zeros = "0000"
        elif player.score < 1000:
            zeros = "000"
        elif player.score < 10000:
            zeros = "00"
        elif player.score < 100000:
            zeros = "0"
        else:
            zeros = ""

        string = "SCORE-" + zeros + str(player.score)
        render = self.font.render(string, False, self.text_color)
        self.background.blit(render, (0,0))

class WeaponNameElement(engine.gui.HudElement):
    """ Displays the current weapon's name """
    
    def __init__(self, game, size, pos):
        engine.gui.HudElement.__init__(self, game, size, pos)
        
    def update(self, player):
        self.background.fill((0,0,0))
        weapon = player.current_weapon.name
        string = "GUN-" + weapon
        render = self.font.render(string, False, self.text_color)
        self.background.blit(render, (0,0))


        