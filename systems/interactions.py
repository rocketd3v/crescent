import pygame

class interactions():
    def __init__(self, interactables):
        self.interactables = interactables
        self.active_interactable = None
        self.dialog = ""
        self.dialog_active = False

    def check_nearby(self, player):
        self.active_interactable = None
        for interactable in self.interactables:
            self.player_cx = player.x + player.width / 2
            self.player_cy = player.y + player.height / 2

            self.player_center = (self.player_cx, self.player_cy)

            expanded_interactable = interactable["rect"].inflate(96, 96)
            nearby = expanded_interactable.collidepoint(self.player_center)

            if nearby:
                self.active_interactable = interactable
                return True

        return False

    def start_interaction(self):
        if self.active_interactable != None:
            self.dialog_active = True
            self.dialog = "The water is completely still..."

    def draw_dialog(self, screen):
        if self.dialog_active:
            self.dialog_rect = pygame.Rect(40, screen.get_height() - 180, screen.get_width() - 80, 140) # height , x, y, width
            pygame.draw.rect(screen, (20, 20, 30), self.dialog_rect)
