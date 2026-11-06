
import pygame
from settings import *
from assets.colours import *

class menu():
    def __init__(self):
        self.options = ["1. New game", "2. Continue", "3. Settings", "4. Quit    "]
        self.option = 0

    def menu_selection(self, event): # this is called a method btw
        if event.type == pygame.KEYDOWN: # menu selection
            if event.key == pygame.K_UP: # up arrow 
                self.option -= 1
                if self.option < 0:
                    self.option = len(self.options) - 1

            elif event.key == pygame.K_DOWN or event.key == pygame.K_TAB: # down arrow
                self.option += 1
                if self.option > len(self.options) - 1:
                    self.option = 0

            elif event.key == pygame.K_RETURN:
                return self.option # code for when option selected

    def draw_menu(self, screen, settings_screen):
        title_font = pygame.font.Font(settings_screen.font_path, 76)
        menu_font = pygame.font.Font(settings_screen.font_path, 46)

        title_surface = title_font.render("CRESCENT", True, gray)
        title_rect = title_surface.get_rect()
        title_rect.centerx = screen_width / 2
        title_rect.centery = screen_height / 8

        screen.blit(title_surface, title_rect)

        for option in range(len(self.options)):
            if option == self.option:
                option_surface = menu_font.render(f"> {self.options[option]}", True, yellow)
            else:
                option_surface = menu_font.render(f"{self.options[option]}", True, black)

            option_rect = option_surface.get_rect()
            option_rect.centerx = screen_width / 2
            option_rect.centery = (screen_height / 4) + (option * 60)
            screen.blit(option_surface, option_rect)
