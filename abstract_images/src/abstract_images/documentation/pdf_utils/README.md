# `pdf_utils.py` - PDF Utilities Module README

---

## Module Information:

- **Module Name:** pdf_utils.py
- **Author:** putkoff
- **GitHub:** [https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images](https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_images)
- **Email:** [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com)
- **Date:** 08/27/2023
- **Version:** 0.0.0.1
- **Part of:** `abstract_images` package

---

## Description:

The `pdf_utils.py` module provides a collection of utility functions for PDF processing. This includes reading, writing, splitting, converting to images, and OCR operations using Tesseract.

---

## Dependencies:

- os
- PyPDF2
- pytesseract
- PIL (Image)
- pdf2image (convert_from_path)
- reportlab (canvas)
- abstract_utilities (various utilities)

---

## Function Descriptions:

- `if_none_return(obj, obj_2)`: Checks and returns the primary object if the secondary object is `None`.
  
- `write_pdf()`: Initializes and returns a new PDF writer object.

- `read_pdf(file)`: Reads a PDF from a given path and returns a PDF reader object.

- `is_pdf_path(file)`: Determines if a given file path corresponds to a valid PDF file.

- `get_pdf_obj(pdf_obj)`: Processes a given PDF object or file path and returns its content.

- `split_pdf(input_path, output_folder, file_name)`: Splits a PDF file into separate pages, saved as individual files.

- `pdf_to_img_list(pdf_list, output_folder, file_name, paginate, extension)`: Converts a list of PDF files into images.

- `img_to_txt_list(img_list, output_folder, file_name, paginate, extension)`: Converts a list of images to text using OCR.

- `open_pdf_file(pdf_file_path)`: Opens a PDF file using the default system application.

- `image_to_text(image_path)`: Converts an image to text using Tesseract OCR.

- `get_pdfs_in_directory(directory)`: Returns a list of PDF filenames in a directory.

- `get_all_pdf_in_directory(file_directory)`: Retrieves full paths of all PDFs in a directory.

- `collate_pdfs(pdf_list, output_pdf_path)`: Merges a list of PDFs into one.

---

## Example Usage:

To demonstrate the capabilities of the `pdf_utils` module, below is an example showcasing the combination of several utility functions:

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

---

## Notes:

- Ensure you have all the required dependencies installed.
- For OCR operations, ensure that Tesseract is properly set up and the path is correctly specified.

For further information or any issues related to this module, feel free to reach out to us at [partners@abstractendeavors.com](mailto:partners@abstractendeavors.com).
