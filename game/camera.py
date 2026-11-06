
class camera():
    def __init__(self, world_width, world_height):
        self.x = 0
        self.y = 0

        self.world_width = world_width
        self.world_height = world_height

    def update(self, player, screen):
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Calculate camera position
        self.x = (
            player.x
            + player.width / 2
            - screen_width / 2
        )

        self.y = (
            player.y
            + player.height / 2
            - screen_height / 2
        )

        # Keep camera inside map boundaries
        self.x = max(
            0,
            min(self.x, self.world_width - screen_width)
        )

        self.y = max(
            0,
            min(self.y, self.world_height - screen_height)
        )
