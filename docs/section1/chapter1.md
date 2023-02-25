# Basic image handling

In this chapter, we will learn basic image operations such as reading, writing,
displaying, and saving images. We will also learn how to convert images to grayscale and
how to resize images.

## Reading images

OpenCV provides the `cv2.imread()` function to read images. The function takes two
arguments: the path to the image and a flag that specifies the way in which image should
be read. Of the many flags, the most useful ones are:

- `cv2.IMREAD_COLOR`: Reads a color image. Any transparency of image will be neglected.
  It is the default flag.
- `cv2.IMREAD_GRAYSCALE`: Reads image in grayscale mode.
- `cv2.IMREAD_ANYCOLOR`: Reads image either as grayscale or color depending on metadata.
- `cv2.IMREAD_UNCHANGED`: Reads all image data, including the fourth channel (alpha
  channel) if it exists.

=== "OpenCV"

    ```python title="Reading images"
    import cv2

    # Read image in color mode
    img = cv2.imread('path/to/image', cv2.IMREAD_COLOR)
    ```

    Note that the image is read in BGR mode by default. If you want to read the image in
    RGB mode, you can use the `cv2.cvtColor()` function to convert the image from BGR to
    RGB.

    ```python title="Converting BGR to RGB"
    import cv2

    # Read image in color mode
    img = cv2.imread('path/to/image', cv2.IMREAD_COLOR)

    # Convert image from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ```

=== "Pillow"

    ```python title="Reading images"
    from PIL import Image

    # Read image in color mode
    img = Image.open('path/to/image')
    ```

## Converting images to grayscale

=== "OpenCV"

    The `cv2.cvtColor()` function can be used to convert images from one color space to
    another. The function takes two arguments: the image to be converted and the flag
    specifying the color space conversion. In the following example, we will convert an
    image from BGR (the default colorscale for OpenCV) to grayscale.

    ```python title="Converting images to grayscale"
    import cv2

    # Read image in color mode
    img = cv2.imread('path/to/image', cv2.IMREAD_COLOR)

    # Convert image from BGR to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ```

=== "Pillow"

    ```python title="Converting images to grayscale"
    from PIL import Image

    # Read image in color mode
    img = Image.open('path/to/image')

    # Convert image from RGB to grayscale
    img = img.convert('L')
    ```

## Displaying images

=== "Matplotlib"

    ```python title="Displaying color images"
    import matplotlib.pyplot as plt

    # Read image into a numpy array
    img: np.ndarray = ...

    # Display image
    plt.imshow(img)
    plt.show()
    ```
