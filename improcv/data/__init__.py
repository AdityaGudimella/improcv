import abc
import typing as t
from pathlib import Path

import numpy as np
import requests
import skimage
from PIL import Image

DATA_DIR = Path(__file__).parent.resolve().absolute()

T = t.TypeVar("T")


class Data(abc.ABC, t.Generic[T]):
    """Base class for any image / video data used in this package."""

    @abc.abstractclassmethod
    def load(self) -> T:
        """Load the data.

        Returns:
            T: The data.
        """
        raise NotImplementedError


class DownloadedData(Data[T]):
    """Base class for data used in this package that is downloaded from internet."""

    def __init__(self, parent_dir: Path, name: str) -> None:
        """Initialize the data.

        Args:
            parent_dir (Path): The path of the directory containing the data.
            name (str): The name of the data file.
        """
        self._parent_dir = parent_dir
        self._name = name
        self._path = (parent_dir / name).resolve().absolute()

    @property
    def name(self) -> str:
        """Get the name of the data.

        Returns:
            str: The name of the data.
        """
        return self._name

    @property
    def path(self) -> Path:
        """Get the path of the data.

        Returns:
            Path: The path of the data.
        """
        return self._path

    @abc.abstractclassmethod
    def download(self) -> None:
        """Download the data."""
        raise NotImplementedError

    def _download_if_needed(self) -> None:
        """Download the data if it does not exist locally."""
        if not self.path.exists():
            self.download()


class ImageFromSkImage(Data[np.ndarray]):
    """An image that is part of a third-party package."""
    def __init__(self, name: str) -> None:
        """Initialize the image.

        Args:
            module (ModuleType): The module containing the image.
        """
        self._module = skimage.data
        self._name = name

    @property
    def name(self) -> str:
        """Get the name of the image.

        Returns:
            str: The name of the image.
        """
        return self._name

    def load(self) -> np.ndarray:
        """Load the image as a numpy array.

        Returns:
            np.ndarray: The image as a numpy array.
        """
        return getattr(self._module, self._name)()


class ImageFromUrl(DownloadedData[np.ndarray]):
    """An image."""

    def __init__(self, parent_dir: Path, name: str, url: str) -> None:
        """Initialize the image.

        Args:
            parent_dir (Path): The path of the directory containing the image.
            name (str): The name of the image file.
            url (str): The URL of the image.
        """
        super().__init__(parent_dir=parent_dir, name=name)
        self._url = url

    def load(self) -> np.ndarray:
        """Load the image as a numpy array.

        Returns:
            np.ndarray: The image as a numpy array.
        """
        self._download_if_needed()
        assert self.path.exists()
        image = Image.open(self.path)
        return np.asarray(image.convert(mode="RGB"))

    def download(self) -> None:
        """Download the image."""
        response = requests.get(self._url)
        with open(self.path, "wb") as f:
            f.write(response.content)


class _Images(t.Collection[Data[np.ndarray]]):
    """A collection of images."""

    def __init__(self) -> None:
        """Initialize the images."""
        self._base_dir = DATA_DIR
        self._images: t.Sequence[Data[np.ndarray]] = []
        self._names: list[str] = []

        # The images
        # # Images from skimage
        self.astronaut = ImageFromSkImage(name="astronaut")
        self._images.append(self.astronaut)
        self._names.append(self.astronaut.name)

        # # Images from the internet
        self.lena: ImageFromUrl = ImageFromUrl(
            parent_dir=self._base_dir,
            name="lena.gif",
            url="https://www.cosy.sbg.ac.at/~pmeerw/Watermarking/lena_color.gif",
        )
        self._images.append(self.lena)
        self._names.append(self.lena.name)

    def __iter__(self) -> t.Iterator[Data[np.ndarray]]:
        """Iterate over the images.

        Returns:
            t.Iterator[ImageFromUrl]: An iterator over the images.
        """
        return iter(self._images)

    def __len__(self) -> int:
        """Get the number of images.

        Returns:
            int: The number of images.
        """
        return len(self._images)

    def __contains__(self, item: str) -> bool:
        """Check if the image collection contains an image.

        Args:
            item (str): The name of the image.

        Returns:
            bool: True if the image collection contains the image, False otherwise.
        """
        return item in self._names


Images = _Images()
