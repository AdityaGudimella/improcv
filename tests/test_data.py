import typing as t
from pathlib import Path

import numpy as np
import pytest

from improcv.data import DownloadedData, Images


@pytest.fixture()
def test_images(tmp_path: Path) -> t.Collection[DownloadedData[np.ndarray]]:
    result = tmp_path / "data"
    result.mkdir()
    Images._base_dir = result
    return Images


def test_load(test_images: t.Collection[DownloadedData[np.ndarray]]) -> None:
    """Test that loading an image downloads it if it does not exist."""
    for image in test_images:
        image.load()
        assert image.path.exists()
