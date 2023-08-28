Sure! Below is a `README.md` for the `image_utils.py` module from the `abstract_images` package.

---

## `image_utils.py` - Image Utilities Module
### Part of the `abstract_images` package.

**Author**: putkoff  
**GitHub Repository**: [abstract_essentials](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images)  
**Contact Email**: [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com)  
**Date**: 08/27/2023  
**Version**: 0.0.0.1  

### Description:
This module provides a range of utilities for working with images, including loading and saving images, extracting text from images, capturing screenshots, and more.

### Dependencies:
- OpenCV
- numpy
- pytesseract
- pyscreenshot
- PIL

### Key Functions:

#### Paths to Image Data:

- **get_dimensions(image_path: str)**: Return dimensions (height, width) of the image.
- **img_to_str(image_path: str)**: Convert image to text using pytesseract.
- **get_pix(image_path: str)**: Return pixel data of the image.
- **image_to_bytes(image_path: str, format: str = "PNG")**: Convert an image at the given path to bytes.
- **get_pixel_data(image_path: str)**: Get pixel data from the image and save the resultant image.
- **open_image(image_path: str)**: Open and return the image using PIL.
- **read_image(image_path: str)**: Read image using OpenCV and return it as a numpy array.

#### Paths to Save:

- **save_url_img(url: str , image_path:str, format: str = "PNG")**: Downloads an image from the specified URL and saves it to the given path.
- **screenshot(image_path: str = "screenshot.png")**: Take a screenshot and save it.
- **save_image(image:Union[Image.Image, ndarray], image_path:str,format:str="PNG")**: Save an image to the specified path. Supports both PIL Image objects and numpy ndarrays.

#### Data to Image:

- **get_image_bytes(image_data: bytes)**: Convert image data in bytes format to a BytesIO stream.
- **pix_to_img(pixel_data: List[List[Tuple[int, int, int]]], image_path: str = "image.png")**: Convert pixel data to an image and save it.
- **show_image(image: Union[Image.Image, ndarray])**: Display an image. Supports both PIL Image objects and numpy ndarrays.


### Note:
For any queries, bug reports, or feature requests, kindly raise an issue on the [GitHub repository](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images) or contact through the provided email.

---


