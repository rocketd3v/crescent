import pygame
from assets.colours import *

class npc():
    def __init__(self, player_gender, interactables, collision_rects, font_path):
        if player_gender == "Male":
            self.gender = "Female"
            self.name = "Mara"
        else:
            self.gender = "Male"
            self.name = "Elliot"

        self.image = pygame.image.load(f"assets/characters/{self.gender}/down_1.png").convert_alpha()

        if self.gender == "Male":
            self.image = pygame.transform.scale(self.image, (32, 32))
        else:
            self.image = pygame.transform.scale(self.image, (48, 48))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.font = pygame.font.Font(font_path, 20)

        pond = None

        for interactable in interactables:
            if interactable["name"] == "pond":
                pond = interactable["rect"]
                break

        if pond != None:
            self.x = pond.centerx - self.width / 2
            self.y = pond.bottom + 20
        else:
            self.x = 500
            self.y = 500

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        collision_rects.append(self.rect)

        interactables.append(
            {
                "name": npc,
                "class": "character",
                "rect": self.rect
            }
        )

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))

        name_surface = self.font.render(self.name, True, white)

        name_rect = name_surface.get_rect()
        name_rect.centerx = self.x - camera_x + self.width / 2
        name_rect.bottom = self.y - camera_y - 4

        screen.blit(name_surface, name_rect)
