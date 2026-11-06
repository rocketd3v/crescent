
import pygame
from settings import *


class player():
    def __init__(self, name, gender, world_width, world_height, keybinds):
        genders = ["Male", "Female"]
        self.name = name
        self.gender = genders[gender]

        self.keybinds = keybinds

        self.speed = 3
        self.direction = "up"
        self.facing_right = False

        self.animation_frame = 0
        self.moving = False

        self.animation_timer = 0
        self.animation_speed = 150

        self.animations = {
            "down": [],
            "side": [],
            "up": [],
        }

        for direction in self.animations:
            for frame in range(1, 4):
                image = pygame.image.load(
                    f"assets/characters/{self.gender}/{direction}_{frame}.png"
                ).convert_alpha()

                if self.gender == "Male":
                    image = pygame.transform.scale(image, (32, 32))
                else:
                    image = pygame.transform.scale(image, (48, 48))

                self.animations[direction].append(image)

        self.width = self.animations["down"][0].get_width()
        self.height = self.animations["down"][0].get_height()

        self.x = (world_width - self.width) / 2
        self.y = (world_height - self.height) / 2

        self.world_width = world_width
        self.world_height = world_height

    def draw(self, screen, camera_x, camera_y):
        image = self.animations[self.direction][self.animation_frame]

        if self.facing_right:
            image = pygame.transform.flip(image, True, False)

        screen.blit(
            image,
            (self.x - camera_x, self.y - camera_y)
        )

    def movement(self):
        self.moving = False
        keys = pygame.key.get_pressed()

        if keys[self.keybinds["Move up"]] and self.y > 0:
            self.direction = "up"
            self.moving = True
            self.facing_right = False
            self.y = max(0, self.y - self.speed)

        if keys[self.keybinds["Move down"]] and self.y < self.world_height - self.height:
            self.direction = "down"
            self.moving = True
            self.facing_right = False
            self.y = min(self.world_height - self.height, self.y + self.speed)

        if keys[self.keybinds["Move right"]] and self.x < self.world_width - self.width:
            self.direction = "side"
            self.moving = True
            self.facing_right = True
            self.x = min(self.world_width - self.width, self.x + self.speed)

        if keys[self.keybinds["Move left"]] and self.x > 0:
            self.direction = "side"
            self.moving = True
            self.facing_right = False
            self.x = max(0, self.x - self.speed)

        if keys[self.keybinds["Open menu"]]:
            pass  # open pause screen

    def animate(self, dt):
        if self.moving:
            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:
                self.animation_frame = (self.animation_frame + 1) % 3
                self.animation_timer = 0
        else:
            self.animation_frame = 0
            self.animation_timer = 0
