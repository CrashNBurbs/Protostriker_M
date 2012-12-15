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
        if current_time - self.last_shot > self.speed:
            shot = bullets.BasicBullet(player_rect.right - 6,
                             player_rect.centery + 4, self.bullet_image)
            self.sound.play()
            self.last_shot = current_time
        else:
            shot = None
        return shot

class Spreader():
    def __init__(self, game):
        self.sound = game.sound_manager.get_sound('laser')
        self.bullet_image = game.image_manager.get_image('pshot')
        self.speed = 200
        self.last_shot = 0

    def fire(self, current_time, player_rect):
        if current_time - self.last_shot > self.speed:
            shot = bullets.BasicBullet(player_rect.right - 6,
                             player_rect.centery + 4, self.bullet_image)
            self.sound.play()
            self.last_shot = current_time
        else:
            shot = None
        return shot