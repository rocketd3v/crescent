import pygame
from assets.colours import *

class objective_tracker():
    def __init__(self, font_path):
        self.font = pygame.font.Font(font_path, 24)

        self.objectives = ["Exlpore hollow creek", "Find someone who can explain the strange events", "Investigate the strange occurence", "Discover the truth"]

        self.current_objective = 0
        self.completed = False

    def complete_objective(self):
        if self.current_objective < len(self.objectives) -1:
            self.current_objective += 1
        else:
            self.completed = True

    def draw(self, screen):
        if not self.completed:
            text = "Objective: " + self.objectives[self.current_objective]
        else:
            text = "All objectives completed"

        surface = self.font.render(text, True, white)

        background = pygame.Rect(15, 15, surface.get_width() + 30, surface.get_height() + 20)

        pygame.draw.rect(screen, (20, 20, 30), background)

        screen.blit(surface, (30, 25))
