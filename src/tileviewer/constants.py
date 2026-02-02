import numpy as np

BYTES_PER_TILE = 16
BITS_PER_TILE = BYTES_PER_TILE * 8
TILE_PIXEL_SIZE = 8
TILES_PER_ROW = 32
MAX_ROM_SIZE = 4_000_000
SCALED_IMG_WIDTH = 1000

COLOR_CHANNELS = 3
COLORMAP = np.array([
    [15,    16,     15],
    [139,   172,    15],
    [48,    98,     48],
    [155,   188,    15]
], dtype=np.uint8)
