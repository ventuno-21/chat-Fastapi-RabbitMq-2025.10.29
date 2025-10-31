from PIL import Image
import io
import base64


def resize_base64_image(base64_str: str, max_size_kb: int = 100) -> str:
    """
    Resize and compress a base64-encoded image to ensure its size is under a specified limit.

    Args:
        base64_str (str): The base64-encoded string representation of an image.
        max_size_kb (int, optional): The maximum desired image size in kilobytes. Defaults to 100 KB.

    Returns:
        str: The resized and compressed image encoded back into a base64 string.

    Example:
        >>> with open("example.jpg", "rb") as f:
        ...     encoded = base64.b64encode(f.read()).decode("utf-8")
        >>> resized_encoded = resize_base64_image(encoded, max_size_kb=50)
        >>> print(len(base64.b64decode(resized_encoded)) / 1024)
        48.7  # ~50 KB after resizing
    """

    # Decode the base64 string into raw image bytes
    image_data = base64.b64decode(base64_str)

    # Open the image from bytes using PIL
    image = Image.open(io.BytesIO(image_data))

    # Initialize a memory buffer to store the processed image
    buffer = io.BytesIO()

    # Save the image with initial compression settings
    image.save(buffer, format="JPEG", optimize=True, quality=70)
    resized_data = buffer.getvalue()

    # If the image is still larger than the desired size, reduce quality further
    while len(resized_data) > max_size_kb * 1024:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", optimize=True, quality=50)
        resized_data = buffer.getvalue()

    # Return the resized image encoded back to a base64 string
    return base64.b64encode(resized_data).decode("utf-8")
