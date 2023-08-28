import os
import PyPDF2
from typing import List, Optional, Union
from .image_utils import save_image,open_image,image_to_text
from pdf2image import convert_from_path
from abstract_utilities.path_utils import is_file
from abstract_utilities.type_utils import is_str
from abstract_utilities.cmd_utils import cmd_input
from abstract_utilities.read_write_utils import write_to_file
from abstract_utilities.path_utils import (is_file, mkdirs, get_directory, 
                                           get_base_name, split_text, 
                                           get_ext, get_file_name)
def if_none_return(obj: object, obj_2: object) -> object:
    """
    Return obj if obj_2 is None, otherwise return obj_2.
    
    Args:
    obj (Any): Primary object to return.
    obj_2 (Any): Secondary object to check.
    
    Returns:
    Any: obj if obj_2 is None, else obj_2.
    """
    return obj if obj_2 is None else obj_2

def write_pdf() -> PyPDF2.PdfWriter:
    """
    Return a new PDF writer object.
    
    Returns:
    PyPDF2.PdfWriter: New PDF writer object.
    """
    return PyPDF2.PdfWriter()
def read_pdf(file: str) -> PyPDF2.PdfReader:
    """
    Read and return a PDF reader object from the provided file path.
    
    Args:
    file (str): Path to the PDF file.
    
    Returns:
    PyPDF2.PdfReader: PDF reader object.
    """
    return PyPDF2.PdfReader(file)
def is_pdf_path(file: str) -> PyPDF2.PdfReader:
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

def read_pdf(file: str) -> PyPDF2.PdfReader:
    """Read and return a PDF reader object from the provided file path."""
    return PyPDF2.PdfReader(file)
def get_pdf_obj(pdf_obj: Union[str, object]) -> object:
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
def get_separate_pages(pdf_reader, start_page:int=1, end_page:int=None):
    """
    Get specific pages from a PDF and return them as a new PDF object.

    Args:
        pdf_reader (object): The PDF reader object.
        start_page (int, optional): The starting page number. Defaults to 1.
        end_page (int, optional): The ending page number. Defaults to the last page.

    Returns:
        object: A new PDF writer object with the specified pages.
    """
    num_pages = get_pdf_pages(pdf_reader)
    
    # Handling default or out-of-bounds page values
    if end_page is None or num_pages < end_page:
        end_page = num_pages
    elif num_pages < start_page:
        return False
    
    pdf_writer = write_pdf()
    
    for page_num in range(num_pages):
        if start_page <= page_num <= end_page:
            pdf_writer.add_page(pdf_reader.pages[page_num])
    return pdf_writer
def is_pdf_path(file):
    """
    Check if the provided file path corresponds to a valid PDF file.

    Args:
        file (str): File path.

    Returns:
        bool: True if it's a valid PDF path, False otherwise.
    """
    if is_file(file) and get_ext(file).lower() == '.pdf':
        return True
    return False

def get_pdf_pages(pdf_file):
    """
    Get the total number of pages in the PDF.

    Args:
        pdf_file (object/str): PDF reader object or path to a PDF file.

    Returns:
        int: Number of pages in the PDF.
    """
    pdf_file = get_pdf_obj(pdf_file)
    try:
        return len(pdf_file.pages)
    except:
        return False
def save_pdf(output_file_path, pdf_writer):
    """
    Save a PDF writer object to a file.

    Args:
        output_file_path (str): Path to save the PDF.
        pdf_writer (object): PDF writer object to save.
    """
    with open(output_file_path, 'wb') as output_file:
        pdf_writer.write(output_file)
def split_pdf(input_path: str, output_folder: Optional[str] = None, file_name: Optional[str] = None) -> List[str]:
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

            output_file_path = os.path.join(output_folder, f'{file_name}_page_{page_num + 1}.pdf')
            output_img_path = os.path.join(output_folder, f'{file_name}_page_{page_num + 1}.png')
            print(f"Writing to: {output_file_path}")
            pdf_pages.append(output_file_path)
            save_pdf(output_file_path,pdf_writer)
            
    return pdf_pages
def pdf_to_img_list(pdf_list: List[str], output_folder: Optional[str] = None, file_name: Optional[str] = None, 
                    paginate: bool = False, extension: str = "png") -> List[str]:
    """
    Convert a list of PDF files to images.

    Args:
        pdf_list (List[str]): List of paths to PDF files.
        output_folder (str, optional): Directory to save the images. Defaults to PDF's directory.
        file_name (str, optional): Base name for the images. Defaults to PDF's name.
        paginate (bool): Whether to paginate the image names. Defaults to False.
        extension (str): Extension for the image files. Defaults to "png".

    Returns:
        List[str]: List of paths to the created image files.
    """
    image_list=[]
    file_name_start = file_name
    for i, each in enumerate(pdf_list):
        try:
            images = convert_from_path(each)
        except Exception as e:
            print("An error occurred while converting the PDF:", e)
        
        if output_folder is None:
            output_folder = get_directory(each)
        if file_name_start is None:
            file_name = get_file_name(each)
        if paginate:
            file_name=f"{file_name}_Page_{i}"
        
        for i, image in enumerate(images):
            image_output_path = os.path.join(output_folder, f"{file_name}.{extension}")
            image_list.append(image_output_path)
            save_image(image=image, image_path=image_output_path, format=extension.upper())
    return image_list
def img_to_txt_list(img_list: List[str], output_folder: Optional[str] = None, file_name: Optional[str] = None, 
                    paginate: bool = False, extension: str = "txt") -> List[str]:
    """
    Convert a list of image files to text.

    Args:
        img_list (List[str]): List of paths to image files.
        output_folder (str, optional): Directory to save the text files. Defaults to image's directory.
        file_name (str, optional): Base name for the text files. Defaults to image's name.
        paginate (bool): Whether to paginate the text filenames. Defaults to False.
        extension (str): Extension for the text files. Defaults to "txt".

    Returns:
        List[str]: List of paths to the created text files.
    """
    text_list = []
    file_name_start = file_name
    for i, each in enumerate(img_list):
        if output_folder is None:
            output_folder = get_directory(each)
        if file_name_start is None:
            file_name = get_file_name(each)
        if paginate:
            file_name=f"{file_name}_Page_{i}"
        
        text_output = image_to_text(each)
        text_output_path = os.path.join(output_folder, f"{get_file_name(each)}.{extension}")
        text_list.append(text_output_path)
        write_to_file(filepath=text_output_path, contents=text_output)
    return text_list
def open_pdf_file(pdf_file_path: str) -> None:
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


def get_pdfs_in_directory(directory: str) -> List[str]:
    """
    Get a list of PDF filenames in a given directory.
    
    Args:
        directory (str): Path to the directory.
        
    Returns:
        list: List of PDF filenames in the directory.
    """
    pdfs = []
    for filename in os.listdir(directory):
        if is_pdf_path(filename):
            pdfs.append(filename)
    return pdfs

def get_all_pdf_in_directory(file_directory: Optional[str] = None) -> List[str]:
    """
    Get a list of complete paths to PDF files in a given directory.
    
    Args:
        file_directory (str, optional): Path to the directory. 
        
    Returns:
        list: List of paths to PDF files in the directory.
    """
    pdfs=[]
    for filename in sorted(os.listdir(file_directory)):
        if is_pdf_path(filename):
            pdf_path = os.path.join(file_directory, filename)
            if is_file(pdf_path):
                pdfs.append(pdf_path)
    return pdfs

def collate_pdfs(pdf_list: List[str], output_pdf_path: str) -> None:
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
    save_pdf(output_file_path, pdf_writer)

