from pathlib import Path

import numpy as np
import numpy.typing as npt
from bitarray import bitarray

from tilechen.constants import (
    BITS_PER_TILE,
    BYTES_PER_TILE,
    COLOR_CHANNELS,
    MAX_ROM_SIZE,
    TILE_PIXEL_SIZE,
    TILES_PER_ROW,
)
from tilechen.exceptions import MaxROMSizeExceededError
from tilechen.model.palettes import DEFAULT_PALETTE, ColorPalette
from tilechen.model.tile import Tile


class TileMap:
    def __init__(self, tiles: list[Tile]) -> None:
        self.tiles = tiles

    @staticmethod
    def read_rom(path: Path) -> "TileMap":
        rom_size = path.stat().st_size
        if rom_size > MAX_ROM_SIZE:
            raise MaxROMSizeExceededError(f"{path.name} exceeds the size limit of {rom_size} bytes!")

        with path.open("rb") as fp:
            rom = bitarray(fp.read())

        tiles = []
        num_tiles = rom.nbytes // BYTES_PER_TILE
        for n in range(num_tiles):
            tile_start_address = n * BITS_PER_TILE
            tile_end_address = (n + 1) * BITS_PER_TILE

            tile_bit_array = rom[tile_start_address:tile_end_address]
            tile = Tile.from_bitarray(tile_bit_array)
            tiles.append(tile)

        return TileMap(tiles)

    def to_rgb(self, color_palette: ColorPalette = DEFAULT_PALETTE) -> npt.NDArray[np.uint8]:
        rgb_tiles = [tile.to_rgb(color_palette) for tile in self.tiles]

        img_height = (len(rgb_tiles) // TILES_PER_ROW) * TILE_PIXEL_SIZE
        img_width = TILE_PIXEL_SIZE * TILES_PER_ROW
        img = np.zeros([img_height, img_width, COLOR_CHANNELS], dtype=np.uint8)

        for index, tile in enumerate(rgb_tiles):
            row, col = divmod(index, TILES_PER_ROW)
            row_start = row * TILE_PIXEL_SIZE
            row_end = row_start + TILE_PIXEL_SIZE
            col_start = col * TILE_PIXEL_SIZE
            col_end = col_start + TILE_PIXEL_SIZE

            img[row_start:row_end, col_start:col_end] = tile

        return img
