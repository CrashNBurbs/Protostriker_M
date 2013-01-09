#-----------------------------------------------------------------------------
#  hud.py
#  contains all the classes for HUD elements and the HUD itself
#-----------------------------------------------------------------------------

import engine

class GameHud(engine.gui.Hud):

    def __init__(self, game, player, color):
        engine.gui.Hud.__init__(self, game, player, color)
        score = ScoreElement(game, (96,8), (0,4), color)
        gun = WeaponNameElement(game, (88,8), (110,4), color)
        level = LevelElement(game, (56,8), (264, 4), color)
        self.elements.append(score)
        self.elements.append(gun)
        self.elements.append(level)

class ScoreElement(engine.gui.HudElement):
    """ Player score """

    def __init__(self, game, size, pos, color):
        engine.gui.HudElement.__init__(self, game, size, pos, color)
        
    def update(self, *args):
        engine.gui.HudElement.update(self)

        player = args[0]

        # append leading zeros based on to always show score
        # out to six places
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

        # build string and score render
        string = "SCORE-" + zeros + str(player.score)
        render = self.font.render(string, False, self.text_color)
        self.background.blit(render, (0,0))

class WeaponNameElement(engine.gui.HudElement):
    """ Displays the current weapon's name """
    
    def __init__(self, game, size, pos, color):
        engine.gui.HudElement.__init__(self, game, size, pos, color)
        
    def update(self, *args):
        engine.gui.HudElement.update(self)
        player = args[0]

        # get players current weapon name, build string and render
        weapon = player.current_weapon.name
        string = "GUN-" + weapon
        render = self.font.render(string, False, self.text_color)
        self.background.blit(render, (0,0))

class LevelElement(engine.gui.HudElement):
    """ Displays the current level """

    def __init__(self, game, size, pos, color):
        engine.gui.HudElement.__init__(self, game, size, pos, color)

    def update(self, *args):
        engine.gui.HudElement.update(self)
        game = args[1]

        # get the game's current level, build string and render
        level = game.current_level
        string = "LEVEL " + str(level)
        render = self.font.render(string, False, self.text_color)
        self.background.blit(render, (0,0))




        