from abstract_webtools import try_request
from typing import Union, List, Tuple
from PIL import Image, PngImagePlugin
import pyscreenshot as ImageGrab
import numpy as np
from numpy import ndarray
from io import BytesIO,_io
import pytesseract
import cv2

#from paths
def get_dimensions(image_path: str) -> Tuple[int, int]:
    """
    Return dimensions (height, width) of the image.

    :param image_path: Path to the image.
    :return: Image dimensions (height, width).
    """
    return read_image(image_path).shape[:-1]

def img_to_str(image_path: str) -> str:
    """
    Convert image to text using pytesseract.

    :param image_path: Path to the image.
    :return: Extracted text from the image.
    """
    img_array = np.array(Image.open(image_path))
    return pytesseract.image_to_string(img_array)

def get_pix(image_path: str) -> object:
    """
    Return pixel data of the image.

    :param image_path: Path to the image.
    :return: Image load object containing pixel values.
    """
    return open_image(image_path).load()

def image_to_bytes(image_path: str, format: str = "PNG") -> bytes:
    """
    Convert an image at the given path to bytes.

    :param image_path: Path to the image file.
    :param format: The format to save the image in. Default is "PNG".
    :return: Bytes representation of the image.
    """
    with Image.open(image_path) as image:
        with BytesIO() as bio:
            save_image(image=image, image_path=bio,format=format)
            return bio.getvalue()
def get_pixel_data(image_path: str) -> List[List[Tuple[int, int, int]]]:
    """
    Get pixel data from the image and save the resultant image.

    :param image_path: Path to the image.
    :return: 2D list containing pixel values.
    """
    dimensions = get_dimensions(image_path)
    px = get_pix(image_path)
    pixel_data = [[px[x, y] for x in range(dimensions[1])] for y in range(dimensions[0])]
    pix_to_img(pixel_data)
    return pixel_data
def open_image(image_path: str) -> Image.Image:
    """
    Open and return the image using PIL.

    :param image_path: Path to the image.
    :return: Image object.
    """
    return Image.open(image_path)

def read_image(image_path: str) -> ndarray:
    """
    Read image using OpenCV and return it as a numpy array.

    :param image_path: Path to the image.
    :return: Image as a numpy array.
    """
    return cv2.imread(image_path)

#to path
def save_url_img(url: str , image_path:str, format: str = "PNG") -> None:
    """
    Downloads an image from the specified URL and saves it to the given path.

    :param path: Path to save the downloaded image.
    :param url: URL of the image to download.
    """
    try:
        response = try_request(url)
        image_data = get_image_bytes(response.content)
        image = open_image(image_data)
        save_image(image=image, image_path=image_path,format=format)
    except requests.RequestException as e:
        print(f"Error fetching image from URL: {e}")
    except Exception as e:
        print(f"Error processing image: {e}")
        
def screenshot(image_path: str = "screenshot.png") -> str:
    """
    Take a screenshot and save it.

    :param image_path: Path to save the screenshot. Default is "screenshot.png".
    :return: Path where the screenshot was saved.
    """
    ImageGrab.grab().save(image_path)
    return image_path

def save_image(image:Union[Image.Image, ndarray], image_path:str,format:str="PNG") -> None:
    """
    Save an image to the specified path. Supports both PIL Image objects and numpy ndarrays.

    :param image: Image object or numpy ndarray.
    :param image_path: Path to save the image.
    """
    if isinstance(image, ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image.save(image_path, format=format)
#from data
def get_image_bytes(image_data: bytes) -> BytesIO:
    """
    Convert image data in bytes format to a BytesIO stream.

    This function takes image data in bytes format and converts it into a BytesIO stream,
    which can be used for various image processing tasks or for streaming operations.

    Args:
        image_data (bytes): Image data in bytes format.

    Returns:
        BytesIO: BytesIO stream containing the image data.

    Example:
        image_bytes = get_image_bytes(image_data_bytes)
        image = Image.open(image_bytes)
    """
    return BytesIO(image_data)

def pix_to_img(pixel_data: List[List[Tuple[int, int, int]]], image_path: str = "image.png") -> None:
    """
    Convert pixel data to an image and save it.

    :param pixel_data: List of pixel values.
    :param image_path: Path to save the image. Default is "image.png".
    """
    image_RGB = np.array(pixel_data)
    image = Image.fromarray(image_RGB.astype('uint8')).convert('RGB')
    image.save(image_path)


def show_image(image: Union[Image.Image, ndarray]) -> None:
    """
    Display an image. Supports both PIL Image objects and numpy ndarrays.

    :param image: Image object or numpy ndarray.
    """
    if isinstance(image, ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image.show()


