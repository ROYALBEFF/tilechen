import json

import numpy as np
import numpy.typing as npt

from tilechen.paths import PALETTE_DATA_FILEPATH

type ColorPalette = npt.NDArray[np.uint8]
COLOR_PALETTE_SHAPE = (4, 3)

DEFAULT_PALETTE = np.array([
    [0x0f,  0x10,   0x0f],
    [0x8b,  0xac,   0x0f],
    [0x30,  0x62,   0x30],
    [0x9b,  0xbc,   0x0f]
], dtype=np.uint8)

PALETTE_0 = np.array([
    [0x00,  0x00,   0x00],
    [0x84,  0x31,   0x00],
    [0xff,  0xad,   0x63],
    [0xff,  0xff,   0xff]
], dtype=np.uint8)

PALETTE_1 = np.array([
    [0x00,  0x00,   0x00],
    [0x94,  0x3a,   0x3a],
    [0xff,  0x84,   0x84],
    [0xff,  0xff,   0xff]
], dtype=np.uint8)

PALETTE_2 = np.array([
    [0x00,  0x00,   0x00],
    [0x00,  0x00,   0xff],
    [0x63,  0xa5,   0xff],
    [0xff,  0xff,   0xff]
], dtype=np.uint8)

PALETTE_3 = np.array([
    [0x00,  0x00,   0x00],
    [0x52,  0x52,   0x8c],
    [0x8c,  0x8c,   0xde],
    [0xff,  0xff,   0xff]
], dtype=np.uint8)

PALETTE_4 = np.array([
    [0x00,  0x00,   0x00],
    [0x00,  0x84,   0x00],
    [0x7b,  0xff,   0x31],
    [0xff,  0xff,   0xff]
], dtype=np.uint8)

PALETTE_5 = np.array([
    [0x00,  0x00,   0x00],
    [0x94,  0x3a,   0x3a],
    [0xff,  0x84,   0x84],
    [0xff,  0xff,   0xff]
], dtype=np.uint8)

PALETTE_6 = np.array([
    [0x00,  0x00,   0x00],
    [0x63,  0x00,   0x00],
    [0xff,  0x00,   0x00],
    [0xff,  0xff,   0x00]
], dtype=np.uint8)

PRE_DEFINED_PALETTES = {
    "default": DEFAULT_PALETTE,
    "palette_0": PALETTE_0,
    "palette_1": PALETTE_1,
    "palette_2": PALETTE_2,
    "palette_3": PALETTE_3,
    "palette_4": PALETTE_4,
    "palette_5": PALETTE_5,
    "palette_6": PALETTE_6,
}

def load_available_palettes() -> dict[str, ColorPalette]:
    # TODO add logging
    if not PALETTE_DATA_FILEPATH.exists():
        return PRE_DEFINED_PALETTES

    with PALETTE_DATA_FILEPATH.open() as f:
        palettes = json.load(f)

    user_defined_palettes = {}
    for palette_name, colors in palettes.items():
        if palette_name in PRE_DEFINED_PALETTES:
            continue

        if palette_name in user_defined_palettes:
            continue

        try:
            colors_array = np.array(colors, dtype=np.uint8)
        except:
            continue

        if colors_array.shape != COLOR_PALETTE_SHAPE:
            continue

        user_defined_palettes[palette_name] = colors_array

    return PRE_DEFINED_PALETTES | user_defined_palettes

def save_color_palette(
        palette_name: str,
        colors: ColorPalette,
        overwrite: bool = False
    ) -> dict[str, ColorPalette] | None:
    # TODO add logging
    with PALETTE_DATA_FILEPATH.open("r") as f:
        palettes = json.load(f)

        # pre defined palettes cannot be overwritten
        if palette_name in PRE_DEFINED_PALETTES:
            return None

        if palette_name in palettes and not overwrite:
            return None

        if colors.shape != COLOR_PALETTE_SHAPE:
            return None

        palettes[palette_name] = colors.tolist()

    with PALETTE_DATA_FILEPATH.open("w") as f:
        json.dump(palettes, f)

    return palettes

def remove_color_palette(palette_name: str) -> None:
    with PALETTE_DATA_FILEPATH.open("r") as f:
        palettes = json.load(f)
        if palette_name in palettes:
            del palettes[palette_name]

    with PALETTE_DATA_FILEPATH.open("w") as f:
        json.dump(palettes, f)

    return palettes

def _int_to_rgb(color: int) -> tuple[int, int, int]:
    r = (color >> 16) & 255
    g = (color >> 8) & 255
    b = color & 255
    return r, g, b

def create_color_palette(black: int, light_grey: int, dark_grey: int, white: int) -> ColorPalette:
    return np.array([
        _int_to_rgb(black),
        _int_to_rgb(light_grey),
        _int_to_rgb(dark_grey),
        _int_to_rgb(white),
    ], dtype=np.uint8)
