"""
`image_utils.py` - Image Utilities Module
=========================================

This module provides utility functions for working with images, such as resizing, converting between formats,
fetching pixel data, and more. It is a part of the `abstract_images` package and interfaces with several libraries
such as OpenCV, pytesseract, PIL, and more.

Usage:
    from image_utils import resize_image, cv2_image_to_bytesio, ...

Author: 
    putkoff

GitHub Repository:
    [abstract_essentials](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images)

Contact Email:
    [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com)

Date:
    08/27/2023

Version:
    0.0.0.1
"""
import cv2
import pytesseract
from numpy import ndarray
from io import BytesIO,_io
import pyscreenshot as ImageGrab
from typing import Union, List, Tuple
from PIL import Image, PngImagePlugin
from abstract_webtools import try_request,requests
#from paths
def resize_image(image_path: str, max_width: int, max_height: int) -> bytes:
    """
    Resize the image to fit within the provided dimensions while maintaining its original aspect ratio.
    
    This function resizes the image specified by the path, such that the resultant image
    fits within the bounding box defined by `max_width` and `max_height`. The resizing operation
    maintains the aspect ratio of the original image, which means the resultant image might be
    smaller than the bounding box in one dimension if the other dimension is already at its maximum 
    size. The resized image is returned in PNG format as bytes.

    Args:
        image_path (str): Path to the image file that needs to be resized.
        max_width (int): Maximum width for the resized image.
        max_height (int): Maximum height for the resized image.
    
    Returns:
        bytes: Bytes representation of the resized image in PNG format.
        
    Example:
        resized_data = resize_image('path/to/image.jpg', 100, 150)
        with open('resized_image.png', 'wb') as file:
            file.write(resized_data)
    """
    with Image.open(image_path) as img:
        # Calculate aspect ratio
        aspect = img.width / img.height
        
        # Determine new dimensions
        new_width = min(max_width, int(max_height * aspect))
        new_height = int(new_width / aspect)
        
        # Resize and save to BytesIO
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        with BytesIO() as bio:
            resized_img.save(bio, format="PNG")
            return bio.getvalue()
def cv2_image_to_bytesio(cv2_image: ndarray) -> BytesIO:
    """
    Convert a given OpenCV image to a BytesIO stream.
    
    This function takes an image in OpenCV's native format and returns a BytesIO stream of the image in RGB format.
    Useful for streaming or working with the image using libraries that support PIL format.

    Args:
        cv2_image (ndarray): OpenCV image to be converted.
        
    Returns:
        BytesIO: BytesIO stream containing the image data in RGB format.
    """
    # Convert from BGR (OpenCV) to RGB (PIL)
    cv2_rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv2_rgb_image)
    
    # Convert PIL image to BytesIO
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer


def read_image(image_path: str) -> ndarray:
    """
    Read image using OpenCV and return it as a numpy array.

    :param image_path: Path to the image.
    :return: Image as a numpy array.
    """
    return cv2.imread(image_path)
def get_dimensions(image_path: str) -> Tuple[int, int]:
    """
    Return dimensions (height, width) of the image.

    :param image_path: Path to the image.
    :return: Image dimensions (height, width).
    """
    return read_image(image_path).shape[:-1]
def image_to_text(image_path: str) -> str:
    """
    Convert an image to text using Tesseract OCR.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        str: Extracted text from the image.
    """
    # Specify the path to the Tesseract executable
    # Open an image file
    with open_image(image_path) as img:
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
    return text

def img_to_str(image_path: str) -> str:
    """
    Convert an image to text using pytesseract.
    
    This function is similar to `image_to_text` but uses a different method of processing the image.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        str: Extracted text from the image.
    """
    img_array = numpy.array(Image.open(image_path))
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

#to path
import requests
from PIL import Image
from io import BytesIO
import os

def save_url_img(url: str, image_path: str, format: str = "PNG") -> None:
    """
    Downloads an image from the specified URL and saves it to the provided local path.
    
    Given a URL pointing to an image, this function fetches the image and saves it 
    locally in the specified path with the desired format. By default, the image is saved 
    in PNG format unless specified otherwise.

    Args:
        url (str): URL from which the image needs to be downloaded.
        image_path (str): Local path where the downloaded image should be saved.
        format (str, optional): Desired image format for saving. Defaults to "PNG".
    
    Raises:
        requests.RequestException: If there's an issue with fetching the image from the URL.
        Exception: If there's any other general error.

    Example:
        save_url_img('https://example.com/image.jpg', 'local_image.png', 'PNG')
    """
    try:
        # Fetch the image from the URL
        response = try_request(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Ensure directory exists
        directory = os.path.dirname(image_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_data = get_image_bytes(response.content)
        # Convert the image bytes to an Image object
        image = open_image(image_data)
        
        # Save the image to the specified path in the desired format
        save_image(image=image, image_path=image_path,format=format)

    except requests.RequestException as e:
        print(f"Error fetching image from URL: {e}")
    except Exception as e:
        print(f"Error processing or saving the image: {e}")
def save_url_img(url: str, image_path: str, format: str = "PNG") -> None:
    """
    Downloads an image from the specified URL and saves it to the given path.

    Args:
        url (str): URL of the image to download.
        image_path (str): Path to save the downloaded image.
        format (str, optional): The format to save the image in. Default is "PNG".
    
    Returns:
        None

    Raises:
        requests.RequestException: If there is an issue with fetching the image from the URL.
        Exception: For any other errors during processing.
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

def save_image(image: Union[Image.Image, ndarray], image_path: str, format: str = "PNG") -> None:
    """
    Save an image to the specified path. Supports both PIL Image objects and numpy ndarrays.
    
    Args:
        image (Union[Image.Image, ndarray]): Image object or numpy ndarray to be saved.
        image_path (str): Path to save the image.
        format (str, optional): The format to save the image in. Default is "PNG".
        
    Returns:
        None
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
    image_RGB = numpy.array(pixel_data)
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
