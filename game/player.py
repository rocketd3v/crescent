from settings import *

class player():
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.speed = 3
        self.direction = "up"

