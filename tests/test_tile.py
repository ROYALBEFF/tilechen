import numpy as np
import numpy.typing as npt
import pytest
from bitarray import bitarray
from bitarray.util import int2ba

from tileviewer.model.tile import Tile


@pytest.mark.parametrize("bit_array, expected_result", [
    (int2ba(0, 8), np.zeros(4, dtype=np.uint8)),
    (int2ba(10, 4), np.asarray([2, 2], dtype=np.uint8)),
    (int2ba(10, 8), np.asarray([0, 0, 2, 2], dtype=np.uint8)),
    (int2ba(10, 10), np.asarray([0, 0, 0, 2, 2], dtype=np.uint8)),
    (int2ba(10, 10), np.asarray([0, 0, 0, 2, 2], dtype=np.uint8)),
    (int2ba(63, 6), np.asarray([3, 3, 3], dtype=np.uint8)),
    (int2ba(63, 8), np.asarray([0, 3, 3, 3], dtype=np.uint8)),
])
def test_2bpp(bit_array: bitarray, expected_result: npt.NDArray[np.uint8]) -> None:
    result = Tile._2bpp(bit_array)
    assert np.array_equal(result, expected_result), \
        f"Expected 2-bits-per-pixel decoding of {bit_array} to be {expected_result}, but got {result}!"

@pytest.mark.parametrize("bit_array", [
    bitarray(0),
    bitarray(1),
    bitarray(7),
])
def test_2bpp_error(bit_array: bitarray) -> None:
    with pytest.raises(ValueError):
        Tile._2bpp(bit_array)
