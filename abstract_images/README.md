## `abstract_images` Module - Image and PDF Utilities

### Part of the `abstract_essentials` Package

**GitHub Repository**: [abstract_essentials](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images)  
**Contact Email**: [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com)  
**Date**: 08/27/2023  
**Version**: 0.0.0.1  

This module, part of the `abstract_essentials` package, provides a collection of utility functions for working with images and PDFs, including loading and saving images, extracting text from images, capturing screenshots, processing PDFs, and more.

### Image Utilities - `image_utils.py`

The `image_utils.py` module contains functions for image-related operations.

#### Paths to Image Data:

- **get_dimensions(image_path: str)**: Return dimensions (height, width) of the image.
- **img_to_str(image_path: str)**: Convert image to text using pytesseract.
- **get_pix(image_path: str)**: Return pixel data of the image.
- **image_to_bytes(image_path: str, format: str = "PNG")**: Convert an image to bytes.
- **get_pixel_data(image_path: str)**: Get pixel data from the image and save the resultant image.
- **open_image(image_path: str)**: Open and return the image using PIL.
- **read_image(image_path: str)**: Read image using OpenCV and return it as a numpy array.

#### Paths to Save:

- **save_url_img(url: str , image_path:str, format: str = "PNG")**: Download an image from URL and save it.
- **screenshot(image_path: str = "screenshot.png")**: Take a screenshot and save it.
- **save_image(image:Union[Image.Image, ndarray], image_path:str,format:str="PNG")**: Save an image to the specified path.

#### Data to Image:

- **get_image_bytes(image_data: bytes)**: Convert image data in bytes format to a BytesIO stream.
- **pix_to_img(pixel_data: List[List[Tuple[int, int, int]]], image_path: str = "image.png")**: Convert pixel data to an image and save it.
- **show_image(image: Union[Image.Image, ndarray])**: Display an image.

### PDF Utilities - `pdf_utils.py`
![image](https://github.com/AbstractEndeavors/abstract_essentials/assets/57512254/2cc6874f-b22a-4a3c-82da-0ebb8ee739cd)

The `pdf_utils.py` module provides functions for PDF processing.

#### Function Descriptions:

- `if_none_return(obj, obj_2)`: Return primary object if secondary object is `None`.
- `write_pdf()`: Initialize and return a new PDF writer object.
- `read_pdf(file)`: Read a PDF from a given path and return a PDF reader object.
- `is_pdf_path(file)`: Check if a file path corresponds to a valid PDF file.
- `get_pdf_obj(pdf_obj)`: Process a PDF object or file path and return its content.
- `split_pdf(input_path, output_folder, file_name)`: Split a PDF file into separate pages.
- `pdf_to_img_list(pdf_list, output_folder, file_name, paginate, extension)`: Convert PDF files into images.
- `img_to_txt_list(img_list, output_folder, file_name, paginate, extension)`: Convert images to text using OCR.
- `open_pdf_file(pdf_file_path)`: Open a PDF file using the default system application.
- `image_to_text(image_path)`: Convert an image to text using Tesseract OCR.
- `get_pdfs_in_directory(directory)`: Get a list of PDF filenames in a directory.
- `get_all_pdf_in_directory(file_directory)`: Get full paths of all PDFs in a directory.
- `collate_pdfs(pdf_list, output_pdf_path)`: Merge a list of PDFs into one.

### Example Usage:

To showcase the `pdf_utils` module, here's an example combining several utility functions:

```python
from abstract_images.pdf_utils import (
    get_file_name, get_directory, mkdirs, split_pdf, 
    pdf_to_img_list, img_to_txt_list
)

pdf_path = "path_to_pdf"
file_name = get_file_name(pdf_path)
directory = get_directory(pdf_path)
pdf_folder = mkdirs(os.path.join(directory, file_name))

pdf_split_folder = mkdirs(os.path.join(pdf_folder, "split"))
pdf_list = split_pdf(input_path=pdf_path, output_folder=pdf_split_folder, file_name=file_name)

pdf_Image_folder = mkdirs(os.path.join(pdf_folder, "images"))
img_list = pdf_to_img_list(pdf_list=pdf_list, output_folder=pdf_Image_folder, paginate=False, extension="png")

pdf_Text_folder = mkdirs(os.path.join(pdf_folder, "text"))
text_list = img_to_txt_list(img_list=img_list, output_folder=pdf_Text_folder, paginate=False, extension="txt")
```

### Note:

For queries, bug reports, or feature requests, please raise an issue on the [GitHub repository](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images) or contact us through the provided email: [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com). Ensure that you have the required dependencies installed, and for OCR operations, ensure Tesseract is properly set up and its path is correctly specified.
