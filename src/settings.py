
class Settings:
    show_energy = True
    show_creature_background = False
    show_creature_com = False
    physics_enabled = True

    @staticmethod
    def toggle_energy():
        Settings.show_energy = not Settings.show_energy

    @staticmethod
    def toggle_creature_background():
        Settings.show_creature_background = not Settings.show_creature_background

    @staticmethod
    def toggle_creature_com():
        Settings.show_creature_com = not Settings.show_creature_com

    @staticmethod
    def toggle_physics():
        Settings.physics_enabled = not Settings.physics_enabled