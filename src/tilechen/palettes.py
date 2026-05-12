import json

import numpy as np
import numpy.typing as npt

from tilechen.paths import PALETTE_DATA_FILEPATH

type ColorPalette = npt.NDArray[np.uint8]
COLOR_PALETTE_SHAPE = (4, 3)

# TODO allow custom palettes
# TODO show palette selection as small coloured rectangles

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
    if not PALETTE_DATA_FILEPATH.exists():
        # TODO log error message
        return PRE_DEFINED_PALETTES

    with PALETTE_DATA_FILEPATH.open() as f:
        palettes = json.load(f)

    user_defined_palettes = {}
    for palette_name, colors in palettes.items():
        if palette_name in PRE_DEFINED_PALETTES:
            # TODO log error message
            continue

        if palette_name in user_defined_palettes:
            # TODO log error message
            continue

        try:
            colors_array = np.array(colors, dtype=np.uint8)
        except:
            # TODO log error message
            continue

        if colors_array.shape != COLOR_PALETTE_SHAPE:
            # TODO log error message
            continue

        user_defined_palettes[palette_name] = colors_array

    return PRE_DEFINED_PALETTES | user_defined_palettes

def save_color_palette(palette_name: str, colors: ColorPalette) -> dict[str, ColorPalette] | None:
    with PALETTE_DATA_FILEPATH.open("w") as f:
        palettes = json.load(f)

        # TODO allow overwrite
        if palette_name in palettes:
            # TODO log error message
            return None

        if colors.shape != COLOR_PALETTE_SHAPE:
            # TODO log error message
            return None

        palettes[palette_name] = colors
        json.dump(palettes, f)

        return palettes
