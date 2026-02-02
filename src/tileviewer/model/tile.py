import numpy as np
import numpy.typing as npt
from bitarray import bitarray

from tileviewer.constants import BITS_PER_TILE, BYTES_PER_TILE, COLORMAP, TILE_PIXEL_SIZE
from tileviewer.exceptions import TileShapeMismatchError


class Tile:
    def __init__(self, pixels: npt.NDArray[np.uint8]) -> None:
        if pixels.shape != (TILE_PIXEL_SIZE, TILE_PIXEL_SIZE):
            raise TileShapeMismatchError(
                f"Tile data must be of shape ({TILE_PIXEL_SIZE}, {TILE_PIXEL_SIZE}), "
                f"but got tile data of shape {pixels.shape}!"
            )
        self.pixels = pixels

    @staticmethod
    def _2bpp(bit_array: bitarray) -> npt.NDArray[np.uint8]:
        if len(bit_array) == 0:
            raise ValueError("Cannot apply 2-bits-per-pixel decoding to an empty bit array!")
        if len(bit_array) % 2 != 0:
            raise ValueError("Cannot apply 2-bits-per-pixel decoding to bit array of uneven length!")

        b = [int(bit_array[i*2:(i*2)+2].to01(), 2) for i in range(len(bit_array) // 2)]
        return np.asarray(b, dtype=np.uint8)

    @staticmethod
    def from_bitarray(bit_array: bitarray) -> "Tile":
        if bit_array.nbytes != BYTES_PER_TILE:
            raise ValueError(
                f"Inappropriate number of bytes! Expected {BYTES_PER_TILE} bytes, but got {bit_array.nbytes}!"
            )

        tile_data = bitarray(BITS_PER_TILE)

        most_significant_pixel_bits = bitarray(bit_array.tobytes()[::2])
        tile_data[::2] = most_significant_pixel_bits

        least_significant_pixel_bits = bitarray(bit_array.tobytes()[1::2])
        tile_data[1::2] = least_significant_pixel_bits

        pixels = Tile._2bpp(tile_data)
        pixels = pixels.reshape((TILE_PIXEL_SIZE, TILE_PIXEL_SIZE))

        return Tile(pixels)

    def to_rgb(self) -> npt.NDArray[np.uint8]:
        return COLORMAP[self.pixels]
