import enum
import typing as t

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


class Backend(enum.Enum):
    """The backend used for displaying images."""

    MATPLOTLIB = "matplotlib"
    PLOTLY = "plotly"


def show_image(
    image: np.ndarray,
    title: str = "",
    backend: Backend = Backend.PLOTLY,
    **kwargs: t.Any
) -> None:
    """Show an image.

    Args:
        image (np.ndarray): The image.
        title (str, optional): The title of the image. Defaults to "".
        backend (Backend, optional): The backend to use for displaying the image.
            Defaults to Backend.PLOTLY.
        **kwargs: Additional arguments to pass to the plotting function.
    """
    if backend == Backend.MATPLOTLIB:
        plt.imshow(image, **kwargs)
        plt.title(title)
        plt.show()
    elif backend == Backend.PLOTLY:
        fig = px.imshow(image, title=title, **kwargs)
        fig.show()
    else:
        raise ValueError(f"Unknown backend: {backend}")
