import pygame
import os
from settings import *

class player():
    def __init__(self, name, gender):
        genders = ["Male", "Female"]
        self.name = name
        self.gender = genders[gender]
        self.x = screen_width / 2
        self.y = screen_height / 2
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
                image = pygame.image.load(f"assets/characters/{self.gender}/{direction}_{frame}.png").convert_alpha()

                image = pygame.transform.scale(image, (32, 32))
                self.animations[direction].append(image)

    def draw(self, screen):
        image = self.animations[self.direction][self.animation_frame]

        if self.facing_right:
            image = pygame.transform.flip(image, True, False)
        
        screen.blit(image, (self.x, self.y))

    def movement(self):
        self.moving = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.y > 0:
            self.direction = "up"
            self.moving = True
            self.facing_right = False
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < 720:
            self.direction = "down"
            self.moving = True
            self.facing_right = False
            self.y += self.speed
        if keys[pygame.K_d] and self.x < 965:
            self.direction = "side" # right
            self.moving = True
            self.facing_right = True
            self.x += self.speed
        if keys[pygame.K_a] and self.x > 0:
            self.direction = "side" # left
            self.moving = True
            self.facing_right = False
            self.x-= self.speed
        if keys[pygame.K_ESCAPE]:
            pass # open pause screen

    def animate(self, dt):
        if self.moving:
            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:
                self.animation_frame = (self.animation_frame + 1) % 3
                self.animation_timer = 0
        else:
            self.animation_frame = 0
