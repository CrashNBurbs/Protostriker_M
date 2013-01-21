#-----------------------------------------------------------------------------
#  hud.py
#  contains all the classes for HUD elements and the HUD itself
#-----------------------------------------------------------------------------

import engine

class GameHud(engine.gui.Hud):

    def __init__(self, game, player, color):
        engine.gui.Hud.__init__(self, game, player, color)
        score = ScoreElement(game, (96,8), (8,4), color)
        gun = WeaponNameElement(game, (88,8), (120,4), color)
        level = LevelElement(game, (56,8), (256, 4), color)
        speed = SpeedElement(game, (102,8), (8,16), color)
        power = FireRateElement(game, (102,8), (120,16), color)
        lives = LivesElement(game, (48,8), (256,16), color)
        self.elements.append(score)
        self.elements.append(gun)
        self.elements.append(level)
        self.elements.append(speed)
        self.elements.append(power)
        self.elements.append(lives)

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

class SpeedElement(engine.gui.HudElement):
    """ Displays the current movement speed """

    def __init__(self, game, size, pos, color):
        engine.gui.HudElement.__init__(self, game, size, pos, color)
        self.image = game.image_manager.get_image('hudbars')
        self.empty_bar = self.image[0]
        self.filled_bar = self.image[2]
        self.string = "SPEED"
        self.render = self.font.render(self.string, False, self.text_color)

    def calc_level(self, player):
        # calculate the player's speed level 
        # (0-4), 0 being default speed
        difference = player.speed - player.default_speed
        level = difference / player.speed_increment
        return level

    def update(self, *args):
        engine.gui.HudElement.update(self)
        player = args[0]

        # get the player's speed level
        player_level = self.calc_level(player)
        
        # draw the string
        self.background.blit(self.render, (0,0))

        # start drawing bars after the string + 3px
        x = self.render.get_width() + 3
        for level in xrange(1,4):
            # draw one empty bar for each possible speed level
            self.background.blit(self.empty_bar, (x,0))
            # draw a filled bar on top of empty bar for each speed leve
            # the player actually has
            if player_level >= level:
                self.background.blit(self.filled_bar, (x,0))
            # increase draw pos by width of the bar + 2px
            x += self.empty_bar.get_width() + 2

class FireRateElement(SpeedElement):
    """ Displays the current firing speed """

    def __init__(self, game, size, pos, color):
        SpeedElement.__init__(self, game, size, pos, color)
        self.filled_bar = self.image[1]
        self.string = "POWER"
        self.render = self.font.render(self.string, False, self.text_color)

    def calc_level(self, player):
        # calculate the player's current weapon level 
        # (0-4), 0 being default speed
        weapon = player.current_weapon
        difference = weapon.default_speed - weapon.speed
        level = difference / weapon.speed_increment
        return level

class LivesElement(engine.gui.HudElement):
    """ Displays the current number of remaining lives """

    def __init__(self, game, size, pos, color):
        engine.gui.HudElement.__init__(self, game, size, pos, color)
        self.image = game.image_manager.get_image('smallship')

    def update(self, *args):
        engine.gui.HudElement.update(self)
        player = args[0]

        # get the number of lives remaining,
        # build string and render
        lives = player.lives
        string = " X " + str(lives)
        render = self.font.render(string, False, self.text_color)

        # draw small ship and render to background
        self.background.blit(self.image, (0,0))
        self.background.blit(render, (self.image.get_width(), 0))











        