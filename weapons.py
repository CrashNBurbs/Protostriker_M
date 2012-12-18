#-----------------------------------------------------------------------------
#  weapons.py
#  contains all the classes for different player weapons
#-----------------------------------------------------------------------------
import bullets

class BasicWeapon():
    """ The players basic weapon - fires a single shot at a time """

    def __init__(self, game):
        self.sound = game.sound_manager.get_sound('laser')
        self.bullet_image = game.image_manager.get_image('pshot')
        self.speed = 200 # delay for creating shots
        self.last_shot = 0 # time of last shot
        
    def fire(self, current_time, player_rect):
        shots = []
        if current_time - self.last_shot > self.speed:
            shot = bullets.BasicBullet(player_rect.right - 6,
                             player_rect.centery, self.bullet_image)
            shots.append(shot)
            self.sound.play()
            self.last_shot = current_time
        return shots

class Spreader():
    """ Spreader weapon - Fire three shots simultaneously """

    def __init__(self, game):
        self.sound = game.sound_manager.get_sound('spreader')
        self.bullet_image = game.image_manager.get_image('spreadshot')
        self.speed = 400
        self.last_shot = 0
        self.angles = [0, 10, 350]

    def fire(self, current_time, player_rect):
        # set shots to empty list if not shooting
        shots = []

        # shoot at a delay of self.speed
        if current_time - self.last_shot > self.speed:
            # create a spreader bullet at angle, append it to shots
            for angle in self.angles:
                shot = bullets.SpreaderBullet(player_rect.centerx,
                                      player_rect.centery, angle, 
                                      self.bullet_image)
                shots.append(shot)
            self.sound.play()
            self.last_shot = current_time
        return shots

class ReverseFire(Spreader):
    """ fires a single straight shot and two reverse shots at an angle """

    def __init__(self, game):
        Spreader.__init__(self, game)
        self.sound = game.sound_manager.get_sound('laser')
        self.bullet_image = game.image_manager.get_image('pshot')
        self.speed = 200
        self.angles = [0, 140, 220]

    def fire(self, current_time, player_rect):
        shots = []

        if current_time - self.last_shot > self.speed:
            for angle in self.angles:
                shot = bullets.ReverseFireBullet(player_rect.right - 6, 
                                                 player_rect.centery, angle,
                                                 self.bullet_image)
                shots.append(shot)
                self.sound.play()
                self.last_shot = current_time
        return shots