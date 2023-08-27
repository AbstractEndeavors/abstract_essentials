import os
import PyPDF2
from abstract_gui import get_browser
from abstract_gui import *
from abstract_utilities.type_utils import*
def is_pdf_path(file):
    if os.path.isfile(file):
        if get_ext(file) == '.pdf':
            return True
    return False
def get_pdf_obj(pdf_obj):
    if is_str(pdf_obj):
        if is_pdf_path(pdf_obj):
            pdf_obj = read_pdf(pdf_obj)
    return pdf_obj
def get_file_path(path):
    return path[:-len(os.path.basename(path))]
def get_ext(file):
    return os.path.splitext(os.path.basename(file))[1]
def read_pdf(file):
    return PyPDF2.PdfReader(file)
def get_pdf_pages(pdf_file):
    pdf_file = get_pdf_obj(pdf_file)
    try:
        pages = len(pdf_file.pages)
        return pages
    except:
        return False
def get_separate_pages(pdf_reader,start_page:int=1,end_page:int=None):
    num_pages = get_pdf_pages(pdf_reader)
    if end_page ==None:
        end_page = get_pdf_pages(pdf_reader)
    elif num_pages < end_page:
        end_page = get_pdf_pages(pdf_reader)
    elif num_pages < start_page:
        return False
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(num_pages):
        if page_num >= start_page and page_num <= end_page:
            pdf_writer.add_page(pdf_reader.pages[page_num])
    return pdf_writer
def save_pdf(output_file_path,pdf_writer):
    with open(output_file_path, 'wb') as output_file:
        pdf_writer.write(output_file)
def create_input(args):
    return get_gui_fun('Input',args)
def create_frame(title:str='',layout:list=[[]],args:dict={}):
    return get_gui_fun('Frame',{"title":title,"layout":layout,**args})
def get_page_selection_section():
    page_start = create_input({"size":(5,1),"key":"-PAGE_START-","enable_events":True})
    page_end = create_input({"size":(5,1),"key":"-PAGE_END-","enable_events":True})
    page_selection_section = create_frame(title="Section Select",layout = [[page_start,get_gui_fun('T',{"value":"-"}),page_end]])
    return page_selection_section
def folder_select(window=None,path="-PDF_INPUT_LOCATION-"):
    if window != None:
        
        if path in values:
            path = values[path]
    if path == '':
        path = os.getcwd()
    ls_select = []
    list_files = os.listdir(path)
    for each in list_files:
        if get_ext(each) == '.pdf':
            ls_select.append(each)
    window["-PDF_SELECTION-"].update(values=ls_select)
def get_values(window=None,st=''):
    events,values = window.read()
    return values[st]
def print_hey():
    print('hey')
def get_func(name,args):
    return {"type":"get","name":name,"args":args}
def update_values(window,string,value):
    window[string].update(value=value)
def update_values(window, string, value):
    window[string].update(value=value)

def separate_button_action(window):
    pdf_file_path = get_values(window, "-PDF_PATH-")
    output_location = get_values(window, "-PDF_SEPARATE_LOCATION-")
    output_name = get_values(window, "-SEPERATE_FOLDER_NAME-")
    start_page = int(get_values(window, "-PAGE_START-"))
    end_page = int(get_values(window, "-PAGE_END-"))

    if pdf_file_path.endswith('.pdf'):
        pdf_obj = read_pdf(pdf_file_path)
        pdf_writer = get_separate_pages(pdf_obj, start_page=start_page, end_page=end_page)

        output_file_path = os.path.join(output_location, output_name+'.pdf')
        input(output_file_path)

        save_pdf(output_file_path, pdf_writer)
        sg.popup('PDF separation completed successfully!', title='Success')

pdf_selector = [[get_gui_fun('Frame',{"title":"pdf_files","layout":[[get_gui_fun('Listbox',{"values":[],"enable_events":True,"key":"-PDF_SELECTION-","size":(30,10)})]]})]]
choose_pdf_location = [[get_gui_fun("Input",{"key":"-PDF_PATH-","enable_events":True}), get_gui_fun("FolderBrowse",{"key":"-PDF_INPUT_LOCATION-","enable_events":True})]]
test_button = get_gui_fun('Button',{"button_text":"Generate List","key":"-LIST_BUTTON-","enable_events":True})
collate_button = get_gui_fun('Button', {"button_text": "Collate", "key": "-COLLATE_BUTTON-", "enable_events": True})
collate = [[
    get_gui_fun('Frame',{"title":"collate","layout":[[
        get_gui_fun('Button',{"button_text":"separate","key":"-SEPARATE_BUTTON-","enable_events":True}),
        get_gui_fun("Input",{"key":"-SEPERATE_PATH-","enable_events":True}),
        get_gui_fun("FolderBrowse",{"key":"-PDF_SEPARATE_LOCATION-","enable_events":True}),
        
        ],[get_gui_fun("T",{"text":"separate folder name"}),get_gui_fun("Input",{"key":"-SEPERATE_FOLDER_NAME-","enable_events":True})]]})]]
    
         
             
                        
layout = [[test_button,get_page_selection_section()],choose_pdf_location,[pdf_selector],collate]
window = get_window("PDF Manipulator",layout=layout)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == "-LIST_BUTTON-":
        window["-PDF_SELECTION-"].update(values=folder_select(window, values["-PDF_INPUT_LOCATION-"]))
    if "PAGE_" in event:
        pages = get_pdf_pages(os.path.join(values["-PDF_INPUT_LOCATION-"],selected_pdf))
        page_value = int(values[event])
        if page_value > pages:
            update_values(window,event,pages)
        if page_value < 0:
            update_values(window,event,0)
    if event == "-PDF_INPUT_LOCATION-":
        folder_select(window, values["-PDF_INPUT_LOCATION-"])
        window["-COLLATE_FOLDER-"].update(value=values["-PDF_INPUT_LOCATION-"])
    if event == "-PDF_PATH-":
        window["-SEPERATE_PATH-"].update(value=values["-PDF_PATH-"])
        
    if event == "-PDF_SELECTION-":
        selected_pdf = values["-PDF_SELECTION-"][0]
        window["-PDF_PATH-"].update(value=os.path.join(values["-PDF_INPUT_LOCATION-"], selected_pdf))
        window["-SEPERATE_PATH-"].update(value=get_file_path(os.path.join(values["-PDF_INPUT_LOCATION-"], selected_pdf)))
        update_values(window,"-PAGE_START-",0)
        update_values(window,"-PAGE_END-",get_pdf_pages(os.path.join(values["-PDF_INPUT_LOCATION-"],selected_pdf)))

    if event == "-SEPARATE_BUTTON-":
        separate_button_action(window)
    if event == "-COLLATE_FOLDER-":
        selected_collate_folder = values["-COLLATE_FOLDER-"]
        pdf_files_in_folder = get_pdfs_in_directory(selected_collate_folder)
        window["-COLLATE_PDF_LIST-"].update(values=pdf_files_in_folder)

    if event == "-COLLATE_BUTTON-":
        collate_button_action(window)


window.close()
#{"-PDF_INPUT_LOCATION-": {"type": "get","name": "folder_select","args": {"path":{"type": "get","name": "get_value","args": {"st": "-PDF_INPUT_LOCATION-"}}}}})
