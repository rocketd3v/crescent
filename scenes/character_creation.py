import pygame
from assets.colours import *
from settings import *

class character_creation():
    def __init__(self):
        self.name = ""
        self.genders = ["Male", "Female"]
        self.gender = 0
        self.active_fields = ["Name: ", "Gender: ", "Back"]
        self.active_field = 0

    def field_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.active_field -= 1
                if self.active_field < 0: # allows wrapping
                    self.active_field = len(self.active_fields) - 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_TAB:
                self.active_field += 1
                if self.active_field > len(self.active_fields) - 1: # allows wrapping
                    self.active_field = 0
            elif event.key == pygame.K_RETURN and self.active_field == 2:
                return "back"

        return self.active_field

    def name_selection(self, screen, event):
        accepted_chars = ["z", "y", "x", "w", "v", "u", "t", "s", "r", "q", "p", "o", "n", "m", "l", "k", "j", "i", "h", "g", "f", "e", "d", "c", "b", "a", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_",]

        if event.type == pygame.KEYDOWN:
            if event.key != pygame.K_BACKSPACE:
                if len(self.name) < 17 and event.unicode.lower() in accepted_chars:
                    self.name += event.unicode
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

    def draw_character_creation(self, screen):
        title_surface = gluten_title_font.render("Character Creation", True, (144, 144, 144))
        title_rect = title_surface.get_rect()
        title_rect.centerx = screen_width / 2
        title_rect.centery = screen_height / 8

        screen.blit(title_surface, title_rect)

        for field in range(len(self.active_fields)):
            if field == 0:
                text_after_field = self.name
            elif field == 1:
                text_after_field = self.genders[self.gender]
            elif field == 2:
                text_after_field = ""

            if field == self.active_field:
                field_surface = gluten_menu_font.render(f"> {self.active_fields[field]} {text_after_field}", True, yellow)
            else:
                field_surface = gluten_menu_font.render(f"{self.active_fields[field]} {text_after_field}", True, black)

            field_rect = field_surface.get_rect()
            field_rect.centerx = (screen_width / 6) + 60
            field_rect.centery = (screen_height / 4) + (field * 60)

            screen.blit(field_surface, field_rect)
