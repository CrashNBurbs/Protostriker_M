#-----------------------------------------------------------------------------
#  weapons.py
#  contains all the classes for different player weapons
#-----------------------------------------------------------------------------
import bullets

class BasicWeapon():
    """ The players basic weapon - fires a single shot at a time """
    def __init__(self, game):
        self.shoot_sound = game.sound_manager.get_sound('laser')
        self.bullet_image = game.image_manager.get_image('pshot')
        self.shoot_speed = 200 # delay for creating shots
        self.last_shot = 0 # time of last shot

    def fire(self, current_time, player_rect):
        if current_time - self.last_shot > self.shoot_speed:
            shot = bullets.PlayerBullet(player_rect.right - 6,
                             player_rect.centery + 4, self.bullet_image)
            self.shoot_sound.play()
            self.last_shot = current_time
        else:
            shot = None
        return shot