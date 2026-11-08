
import pygame
from assets.colours import *


class npc:
    # Main NPC: Mara or Elliot
    def __init__(self, player_gender, interactables, collision_rects, font_path):

        if player_gender == "Male":
            self.gender = "Female"
            self.name = "Mara"
        else:
            self.gender = "Male"
            self.name = "Elliot"

        self.image = pygame.image.load(
            f"assets/characters/{self.gender}/down_1.png"
        ).convert_alpha()

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

        if pond is not None:
            self.x = pond.centerx - self.width / 2
            self.y = pond.bottom + 20
        else:
            self.x = 500
            self.y = 500

        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )

        collision_rects.append(self.rect)

        interactables.append({
            "name": "npc",
            "class": "character",
            "rect": self.rect
        })

    def draw(self, screen, camera_x, camera_y):

        screen.blit(
            self.image,
            (self.x - camera_x, self.y - camera_y)
        )

        name_surface = self.font.render(self.name, True, white)

        name_rect = name_surface.get_rect()
        name_rect.centerx = self.x - camera_x + self.width / 2
        name_rect.bottom = self.y - camera_y - 4

        screen.blit(name_surface, name_rect)


class house_npc:
    # Static NPCs outside the blue, black and green houses
    def __init__(
        self,
        name,
        house_name,
        interactables,
        collision_rects,
        font_path
    ):

        self.name = name
        self.house_name = house_name

        self.image = pygame.image.load(
            f"assets/characters/{name}/{name}.png"
        ).convert_alpha()

        # Scale the image down whilst preserving proportions
        target_height = 64

        original_width = self.image.get_width()
        original_height = self.image.get_height()

        self.height = target_height
        self.width = int(
            original_width * target_height / original_height
        )

        self.image = pygame.transform.scale(
            self.image,
            (self.width, self.height)
        )

        self.font = pygame.font.Font(font_path, 20)

        # Find the house
        house = None

        for interactable in interactables:
            if interactable["name"] == house_name:
                house = interactable["rect"]
                break

        if house is None:
            raise ValueError(
                f"Could not find interactable: {house_name}"
            )

        # Position NPC outside their house
        self.x = house.centerx - self.width / 2
        self.y = house.bottom - 50

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        # Register collision
        collision_rects.append(self.rect)

        # Register interaction
        interactables.append({
            "name": f"{house_name}_npc",
            "class": "character",
            "rect": self.rect
        })

    def draw(self, screen, camera_x, camera_y):

        screen.blit(
            self.image,
            (self.x - camera_x, self.y - camera_y)
        )

        name_surface = self.font.render(
            self.name,
            True,
            white
        )

        name_rect = name_surface.get_rect()
        name_rect.centerx = self.x - camera_x + self.width / 2
        name_rect.bottom = self.y - camera_y - 4

        screen.blit(name_surface, name_rect)
