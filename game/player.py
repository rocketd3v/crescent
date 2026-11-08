
import pygame
from settings import *
from assets.colours import *


class player():
    def __init__(self, name, gender, world_width, world_height, keybinds, collision_rects, font_path):
        genders = ["Male", "Female"]
        self.name = name
        self.gender = genders[gender]

        self.keybinds = keybinds
        self.collision_rects = collision_rects

        self.speed = 3
        self.direction = "up"
        self.facing_right = False

        self.animation_frame = 0
        self.moving = False

        self.animation_timer = 0
        self.animation_speed = 150

        # Player name font
        self.name_font = pygame.font.Font(font_path, 20)

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

        # Draw player name above head
        name_surface = self.name_font.render(
            self.name, True, white
        )

        name_rect = name_surface.get_rect()

        name_rect.centerx = self.x - camera_x + self.width / 2
        name_rect.bottom = self.y - camera_y - 4

        screen.blit(name_surface, name_rect)

    def movement(self):
        self.moving = False
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[self.keybinds["Move up"]]:
            dy -= self.speed
            self.direction = "up"
            self.facing_right = False

        if keys[self.keybinds["Move down"]]:
            dy += self.speed
            self.direction = "down"
            self.facing_right = False

        if keys[self.keybinds["Move right"]]:
            dx += self.speed
            self.direction = "side"
            self.facing_right = True

        if keys[self.keybinds["Move left"]]:
            dx -= self.speed
            self.direction = "side"
            self.facing_right = False

        if dx != 0 or dy != 0:
            self.moving = True

        # Horizontal movement
        self.x += dx
        player_rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )

        for collision in self.collision_rects:
            if player_rect.colliderect(collision):
                if dx > 0:
                    player_rect.right = collision.left
                elif dx < 0:
                    player_rect.left = collision.right

                self.x = player_rect.x

        # Vertical movement
        self.y += dy
        player_rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )

        for collision in self.collision_rects:
            if player_rect.colliderect(collision):
                if dy > 0:
                    player_rect.bottom = collision.top
                elif dy < 0:
                    player_rect.top = collision.bottom

                self.y = player_rect.y

        # Keep player inside map
        self.x = max(0, min(self.x, self.world_width - self.width))
        self.y = max(0, min(self.y, self.world_height - self.height))

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
