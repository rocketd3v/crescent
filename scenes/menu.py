import pygame

class menu():
    def __init__(self):
        self.options = ["1. New game", "2. Continue", "3. Settings", "4. Quit"]
        self.option = 0

    def menu_selection(self, event): # this is called a method btw
        if event.type == pygame.KEYDOWN: # menu selection
            if event.key == pygame.K_UP: # up arrow 
                self.option -= 1
                if self.option < 0:
                    self.option = len(self.options) - 1
                print(f"option: {self.option}")

            elif event.key == pygame.K_DOWN: # down arrow
                self.option += 1
                if self.option > len(self.options) - 1:
                    self.option = 0
                print(f"option: {self.option}")

class font():
    def __init__(self):
        self.title_font = 0 # idk what to put here
        self.menu_font = 0 #same here
