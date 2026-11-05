from pytmx.util_pygame import load_pygame


class game_map():
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)

        # Map layers (Tiled saved these names in lowercase).
        self.ground_layer = self.tmx_data.get_layer_by_name("ground")
        self.objects_layer = self.tmx_data.get_layer_by_name("objects")

        # Buildings is optional until that layer is added in Tiled.
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

    def draw(self, screen):
        # Draw layers in the same order they appear in Tiled.
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for tile_column, tile_row, image in layer.tiles():
                    pixel_x = tile_column * self.tile_width
                    pixel_y = tile_row * self.tile_height
                    screen.blit(image, (pixel_x, pixel_y))
