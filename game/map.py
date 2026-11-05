# this whole file is ai, it broke and icba to fixs

from pytmx.util_pygame import load_pygame


class game_map():
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)

        self.ground_layer = self.tmx_data.get_layer_by_name("ground")
        self.objects_layer = self.tmx_data.get_layer_by_name("objects")

        self.buildings_layer = next(
            (layer for layer in self.tmx_data.visible_layers
             if layer.name.lower() == "buildings"),
            None
        )

        self.map_width = self.tmx_data.width
        self.map_height = self.tmx_data.height

        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        self.pixel_width = self.map_width * self.tile_width
        self.pixel_height = self.map_height * self.tile_height

    def draw(self, screen, camera_x, camera_y):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for tile_column, tile_row, image in layer.tiles():
                    pixel_x = tile_column * self.tile_width
                    pixel_y = tile_row * self.tile_height

                    screen_x = pixel_x - camera_x
                    screen_y = pixel_y - camera_y

                    screen.blit(image, (screen_x, screen_y))
