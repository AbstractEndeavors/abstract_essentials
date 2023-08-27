from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pdf2image import convert_from_path
import pytesseract
from reportlab.pdfgen import canvas
import os
import PyPDF2
import pytesseract
import subprocess
from PIL import Image
from abstract_utilities.type_utils import is_str
from abstract_utilities.path_utils import is_file
from abstract_utilities.cmd_utils import cmd_input
from abstract_utilities.read_write_utils import write_to_file
from image_utils import save_image
from typing import Union, List

def if_none_return(obj, obj_2):
    """
    Return obj if obj_2 is None, otherwise return obj_2.
    
    Args:
    obj (Any): Primary object to return.
    obj_2 (Any): Secondary object to check.
    
    Returns:
    Any: obj if obj_2 is None, else obj_2.
    """
    return obj if obj_2 is None else obj_2
def get_pdf_pages(pdf_file):
    """
    Return the number of pages in the given PDF file or object.
    
    Args:
    pdf_file (Union[str, PyPDF2.PdfReader]): PDF file path or object.
    
    Returns:
    Union[int, bool]: Number of pages or False if error occurs.
    """
    pdf_file = get_pdf_obj(pdf_file)
    try:
        pages = len(pdf_file.pages)
        return pages
    except:
        return False
def write_pdf():
    """
    Return a new PDF writer object.
    
    Returns:
    PyPDF2.PdfWriter: New PDF writer object.
    """
    return PyPDF2.PdfWriter()
def read_pdf(file):
    """
    Read and return a PDF reader object from the provided file path.
    
    Args:
    file (str): Path to the PDF file.
    
    Returns:
    PyPDF2.PdfReader: PDF reader object.
    """
    return PyPDF2.PdfReader(file)
def sanitize_filename(name: str):
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
    name (str): Filename to sanitize.
    
    Returns:
    str: Sanitized filename.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)
def get_directory(file_path: str) -> str:
    """
    Extracts and returns the directory path from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The directory path extracted from the file path.
    """
    return file_path[:-len(get_base_name(file_path))]

def get_base_name(file_path: str) -> str:
    """
    Extracts and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file.
    """
    return os.path.basename(file_path)
def split_text(string: str) -> tuple:
    """
    Splits a string into its base name and extension and returns them as a tuple.

    Args:
        string (str): A string to be split, typically representing a file name.

    Returns:
        tuple: A tuple containing the base name and extension of the input string.
    """
    return os.path.splitext(string)
def get_ext(file_path: str) -> str:
    """
    Retrieves and returns the extension of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The extension of the file (including the dot).
    """
    return split_text(get_base_name(file_path))[1]
def get_file_name(file_path: str) -> str:
    """
    Retrieves and returns the base name of a file from a given file path.

    Args:
        file_path (str): A string representing the file path.

    Returns:
        str: The base name of the file (without extension).
    """
    return split_text(get_base_name(file_path))[0]
def is_pdf_path(file: str) -> bool:
    """
    Checks if a given file path corresponds to a PDF file.

    Args:
        file (str): A string representing the file path.

    Returns:
        bool: True if the file has a '.pdf' extension, False otherwise.
    """
    if is_file(file):
        if get_ext(file) == '.pdf':
            return True
    return False

def get_pdf_obj(pdf_obj) -> object:
    """
    Processes and returns a PDF object. If provided with a file path to a PDF,
    it reads and returns the PDF content as an object.

    Args:
        pdf_obj: Either a PDF file path or an existing PDF object.

    Returns:
        object: The PDF content as an object.
    """
    if is_str(pdf_obj):
        if is_pdf_path(pdf_obj):
            pdf_obj = read_pdf(pdf_obj)  # Assuming there's a function read_pdf() to read PDF content
    return pdf_obj

def get_pdf_page_count(file_path:str):
    """
    Return the number of pages in the given PDF file.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        int: Number of pages in the PDF.
    """
    pdf_reader = get_pdf_obj(file_path)
    return get_pdf_pages(pdf_reader)

def get_pdf_page(pdf_reader,page_num):
    """
    Extract a specific page from the provided PDF reader object.
    
    Args:
        pdf_reader: A PyPDF2 PdfReader object.
        page_num (int): Page number to extract (0-indexed).
        
    Returns:
        PageObject: The specified page from the PDF.
    """
    return pdf_reader.pages[page_num]




def split_pdf(input_path, output_folder:str=None, file_name:str=None):
    """
    Split a PDF file into separate files for each page.
    
    Args:
        input_path (str): Path to the input PDF file.
        output_folder (str, optional): Directory to save the split PDF files. Defaults to the directory of input_path.
        file_name (str, optional): Base name for the output files. Defaults to the base name of input_path.
        
    Returns:
        list: List of paths to the created split PDF files.
    """
    pdf_pages = []
    file_name = get_file_name(input_path) if file_name is None else file_name
    output_folder = if_none_return(get_directory(input_path), output_folder)  

    print(f"Splitting PDF: {input_path}")
    print(f"Output Folder: {output_folder}")
    print(f"Using Filename: {file_name}")

    with open(input_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)  # Replace getNumPages() with len(pdf_reader.pages)

        print(f"Number of pages in PDF: {num_pages}")

        for page_num in range(num_pages):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])  # Use the pdf_writer instance you created

            output_file_path = os.path.join(output_folder, f'page_{page_num + 1}.pdf')
            output_img_path = os.path.join(output_folder, f'page_{page_num + 1}.png')
            print(f"Writing to: {output_file_path}")
            with open(output_file_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                image = convert_pdf_to_img(read_pdf(output_file_path))
                save_image(image=image,image_path=output_img_path)
                pdf_pages.append(output_file_path)
    return pdf_pages

def convert_pdf_to_img(file_path: str, output_folder: str = None):
    """
    Convert a PDF file into a series of image files.
    
    Args:
        file_path (str): Path to the PDF file.
        output_folder (str, optional): Directory to save the generated image files. Defaults to the directory of file_path.
    """
    output_folder = if_none_return(get_directory(file_path), output_folder)
    try:
        images = convert_from_path(file_path)
    except Exception as e:
        print("An error occurred while converting the PDF:", e)
        return  # Exit the function if an error occurs
    file_name = get_file_name(file_path)
    for i, image in enumerate(images):
        # We save each page as a separate image file
        base_name = f"{file_name}_page{i + 1}.png"
        output_path = os.path.join(output_folder,base_name)
        save_image(image=image, image_path=output_path,format="PNG")        
        return output_path
def open_pdf_file(pdf_file_path:str):
    """
    Open a PDF file using the default associated program.
    
    Args:
        pdf_file_path (str): Path to the PDF file to open.
    """
    try:
        # Open the PDF file using the default associated program
        cmd_input("open "+pdf_file_path)
    except FileNotFoundError:
        print("Error: The specified file does not exist.")
    except Exception as e:
        print("Error:", e)
    # use it before writing to a file
def image_to_text(image_path:str):
    """
    Convert an image to text using Tesseract OCR.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        str: Extracted text from the image.
    """
    # Specify the path to the Tesseract executable
    # Open an image file
    with Image.open(image_path) as img:
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
    return text
    
def sanitize_and_open():
    """
    Sanitize the filename obtained from OCR output and write the content to the file.
    """
    sanitized_filename = sanitize_filename(ocr_output)
    with open(sanitized_filename, 'w', encoding='UTF-8') as f:
        f.write(ocr_output)


def get_pdfs_in_directory(directory):
    """
    Get a list of PDF filenames in a given directory.
    
    Args:
        directory (str): Path to the directory.
        
    Returns:
        list: List of PDF filenames in the directory.
    """
    pdfs = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            pdfs.append(filename)
    return pdfs
def get_all_pdf_in_directory(file_directory:str=None):
    """
    Get a list of complete paths to PDF files in a given directory.
    
    Args:
        file_directory (str, optional): Path to the directory. 
        
    Returns:
        list: List of paths to PDF files in the directory.
    """
    pdfs=[]
    for filename in sorted(os.listdir(file_directory)):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(file_directory, filename)
            if is_file(pdf_path):
                pdfs.append(pdf_path)
    return pdfs
def collate_pdfs(pdf_list, output_pdf_path):
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        pdf_list (list): List of paths to PDF files to be merged.
        output_pdf_path (str): Path to save the merged PDF.
    """
    pdf_writer = PyPDF2.PdfWriter()
    for file_path in pdf_list:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)
def pdf_image_to_pdf_text(pdf_path, output_path):
    """
    Convert a PDF with images into a PDF with extracted text using OCR.
    
    Args:
        pdf_path (str): Path to the source PDF with images.
        output_path (str): Path to save the generated PDF with extracted text.
    """
    # Convert the PDF into images
    images = convert_from_path(pdf_path)

    # Create a new PDF for output
    c = canvas.Canvas(output_path)

    for i, image in enumerate(images):
        # Perform OCR on the image to get the text
        text = pytesseract.image_to_string(image)

        # Add a page to the PDF
        c.showPage()

        # Write the text to the PDF
        c.setFont("Helvetica", 12)  # Set the font to something standard
        for line in text.split('\n'):
            c.drawString(30, 800-i*15, line)

    # Save the output PDF
    c.save()
def overlay_text_on_pdf(image_path, text, boxes_data, output_path):
    """
    Overlay text on a PDF based on provided bounding boxes.
    
    Args:
        image_path (str): Path to the source image (which will be the base for the PDF).
        text (str): Text to overlay on the PDF.
        boxes_data (str): Bounding boxes data for where to overlay the text.
        output_path (str): Path to save the generated PDF with overlaid text.
    """
    # Create a new PDF with Reportlab
    c = canvas.Canvas(output_path, pagesize=letter)

    # Add the image to the PDF
    img = ImageReader(image_path)
    img_width, img_height = img.getSize()
    c.drawImage(img, 0, 0, width=img_width, height=img_height)

    # Overlay text on the PDF using bounding boxes
    if boxes_data.strip():  # Check if the bounding box data is not empty
        # Split the text into individual lines
        lines = text.split('\n')

        # Overlay text on the image using bounding boxes
        for line in boxes_data.splitlines():
            char, left, bottom, right, top, _ = line.split()
            left, bottom, right, top = int(left), int(bottom), int(right), int(top)

            # Replace the region within bounding box with the corresponding text
            for text_line in lines:
                if char in text_line:
                    text_to_overlay = text_line.strip()
                    break
            else:
                text_to_overlay = ""

            if text_to_overlay:
                # Calculate the position for overlaying the text
                text_position = (left, img_height - top - 5)  # You can adjust the vertical offset here

                # Overlay the text on the PDF
                c.drawString(*text_position, text_to_overlay)

    # Save the PDF
    c.save()



#pdf_list = split_pdf(pdf_file_path)

#output_collated_pdf_path = "/home/john-putkey/Documents/modules/abstract_images/src/abstract_images/John_Putkey_Resume_collated.pdf"
#collate_pdfs(pdf_list, output_collated_pdf_path)



pdf_file_path = "path_to_pdf"
output_folder = "output_folder"
pdf_file_path = "/home/john-putkey/Documents/modules/abstract_images/src/abstract_images/John_Putkey_Resume.pdf"
output_folder = "/home/john-putkey/Documents/modules/abstract_images/src/abstract_images/"
pdf_list = split_pdf(pdf_file_path)
input(pdf_list)
for each in pdf_list:
    images = convert_from_path(each)
    print(images)
    save_image(image=images[0],image_path=each[:-len('.pdf')]+'.png')
    path = convert_pdf_to_img(file_path=each,output_folder=output_folder)
    text=image_to_text(image_path=path)
    text_path = path[:-len(get_ext(path))]+'.txt'
    write_to_file(filepath=text_path,contents=text)
output_collated_pdf_path = "output_collated_pdf_path"
collate_pdfs(pdf_list, output_collated_pdf_path)
