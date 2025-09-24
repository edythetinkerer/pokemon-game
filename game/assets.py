"""
This file holds all the in-code asset definitions, like our
pixel art shapes, so we don't need external image files.
"""
# START:ASSETS_PIXEL_ART
"""
This file holds all the in-code asset definitions, like our
pixel art shapes, so we don't need external image files.
"""
# START:ASSETS_PIXEL_ART
def load_pixel_art():
    """
    Defines the shapes of all our game objects as pixel data.
    Returns a dictionary of these shapes.
    '1' = body, '.' = skin, 'g' = grass, 'f' = flower
    't' = tall grass
    """
    player_shape = [
        "      1111      ",
        "     111111     ",
        "     11....11     ",
        "    1.1.1.1.11    ",
        "    1.1.1.1.11    ",
        "    11......11    ",
        "      1111      ",
        "   111111111111   ",
        "  11 111111 11  ",
        " 11  111111  11 ",
        " 1   111111   1 ",
        "     11  11     ",
        "     11  11     ",
        "     11  11     ",
        "    111  111    ",
        "                ",
    ]

    grass_tile_shape = [
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
    ]

    flower_tile_shape = [
        "gggggggggggggggg",
        "ggg f gggggggggg",
        "gg fff ggggggggg",
        "g fffff gggggggg",
        "g fffff gggggggg",
        "gg fff ggggggggg",
        "ggg f gggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
        "gggggggggggggggg",
    ]

    tall_grass_tile_shape = [
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
        "tttttttttttttttt",
    ]

    art = {
        'player': player_shape,
        'grass': grass_tile_shape,
        'flower': flower_tile_shape,
        'tall_grass': tall_grass_tile_shape,
    }
    return art
# END:ASSETS_PIXEL_ART
# END:ASSETS_PIXEL_ART
# END:ASSETS_PIXEL_ART
# END:ASSETS_PIXEL_ART
# END:ASSETS_PIXEL_ART

