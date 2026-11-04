import pygame
from assets.colours import *
from settings import *

class character_creation():
    def __init__(self):
        self.name = ""
        self.genders = ["Male", "Female"]
        self.gender = 0
        self.active_fields = ["name", "gender"]
        self.active_field = 0

    def field_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.active_field -= 1
                if self.active_field < 0: # allows wrapping
                    self.active_field = len(self.active_fields) - 1
            elif event.key == pygame.K_DOWN:
                self.active_field += 1
                if self.active_field > len(self.active_fields) - 1: # allows wrapping
                    self.active_field = 0

    def name_selection(self, screen, event):
        accepted_chars = ["z", "y", "x", "w", "v", "u", "t", "s", "r", "q", "p", "o", "n", "m", "l", "k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_",]
        if self.active_field == 0:
            self.font = pygame.font.Font(gluten_location, 46)

            length_err_surface = self.font.render("Character name should range from 1-16 chracters.", True, red)
            length_err_rect = length_err_surface.get_rect()
            length_err_rect.centerx = screen_width / 6
            length_err_rect.centery = screen_height / 4 # add 60 for gender

            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_BACKSPACE:
                    if len(self.name) < 17 and event.unicode.lower() in accepted_chars:
                        self.name += event.unicode
                    else:
                        screen.blit(length_err_surface, length_err_rect) # arguments are the surface and its rect          
                else:
                    self.name = self.name[:-1]

    def gender_selection(self, event):
        if self.active_field == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.gender += 1
                    if self.gender > 1:
                        self.gender = 0
                elif event.key == pygame.K_LEFT:
                    self.gender -= 1
                    if self.gender < 0:
                        self.gender = 1

    