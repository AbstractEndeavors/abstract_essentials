import os
import .PyPDF2
from abstract_gui import get_browser,create_window_manager,get_window,get_gui_fun,expandable
from pdf_utils import get_directory,get_pdf_obj,get_ext,read_pdf,save_pdf,is_pdf_path,get_separate_pages,get_pdf_pages
from abstract_utilities.type_utils import is_number,ensure_integer
window_mgr,bridge,pdf_module_script_name=create_window_manager(global_var=globals())
js_bridge=bridge.return_global_variables()
js_bridge["selected_pdf"]=''
def get_values(window=None,st:any=None):
    values = window_mgr.get_values()
    print(values)
    if st in values:
        return values[st]
def update_values(window:type(get_window())=None,key:str=None,value=None,args:dict={}):
    window_mgr.update_values(window=window,key=key,value=value,args=args)
def get_page_selection_section():
    page_start = get_gui_fun('Input',{"size":(5,1),"key":"-PAGE_START-","enable_events":True})
    page_end = get_gui_fun('Input',{"size":(5,1),"key":"-PAGE_END-","enable_events":True})
    return get_gui_fun('Frame',{"title":"Section Select","layout":[[page_start,get_gui_fun('T',{"value":"-"}),page_end]]})
def folder_select(window:type(get_window())=None,path:str="-PDF_INPUT_LOCATION-"):
    if window != None:
        if path in window_mgr.get_values():
            path = get_values(window=window, st=path)
    if path == '':
        path = os.getcwd()
    ls_select = []
    list_files = os.listdir(path)
    for each in list_files:
        if get_ext(each) == '.pdf':
            ls_select.append(each)
    update_values(window=window,key="-PDF_SELECTION-",args={"values":ls_select})
def separate_button_action(window):
    pdf_file_path = get_values(window=window, st="-PDF_PATH-")
    output_location = get_values(window=window, st="-PDF_SEPARATE_LOCATION-")
    output_name = get_values(window=window, st="-SEPERATE_FOLDER_NAME-")
    start_page = int(get_values(window=window, st="-PAGE_START-"))
    end_page = int(get_values(window=window, st="-PAGE_END-"))
    if is_pdf_path(pdf_file_path):
        pdf_obj = read_pdf(pdf_file_path)
        pdf_writer = get_separate_pages(pdf_obj, start_page=start_page, end_page=end_page)
        output_file_path = os.path.join(output_location, output_name+'.pdf')
        save_pdf(output_file_path, pdf_writer)
        sg.popup('Success',text='PDF separation completed successfully!')
def while_events(event):
    if event == "-LIST_BUTTON-":
        update_values(window=window,key="-PDF_SELECTION-",args={"values":folder_select(window, get_values(window=window, st="-PDF_INPUT_LOCATION-"))})
    if "PAGE_" in event:
        pages = get_pdf_pages(os.path.join(get_values(window=window,st="-PDF_INPUT_LOCATION-"),js_bridge["selected_pdf"]))
        page_value = window_mgr.get_values(window=window)[event]
        if event == "-PAGE_START-":
            page_value=int(ensure_integer(page_value, 0))
            window_mgr.update_values(window=window,key="-PAGE_START-",value=page_value)
            value_end = ensure_integer(window_mgr.get_values(window=window)["-PAGE_END-"],pages)
            if page_value > value_end:
                update_values(window=window,key="-PAGE_START-",args={"value":value_end})
            if pages < value_end:
                update_values(window=window,key="-PAGE_END-",args={"value":pages})
        else:
            page_value=int(ensure_integer(page_value, pages))
            window_mgr.update_values(window=window,key="-PAGE_END-",value=page_value)
            value_start = ensure_integer(window_mgr.get_values(window=window)["-PAGE_START-"],0)
            if pages < page_value:
                update_values(window=window,key="-PAGE_END-",args={"value":pages})
            if value_start > page_value:
                update_values(window=window,key="-PAGE_START-",args={"value":page_value})
        if page_value > pages:
            update_values(window=window,key=event,args={"value":pages})
        if page_value < 0:
            update_values(window=window,key=event,args={"value":0}) 
    if event == "-PDF_INPUT_LOCATION-":
        folder_select(window, values["-PDF_INPUT_LOCATION-"])
        update_values(window=window,key="-COLLATE_FOLDER-",args={"value":js_bridge["selected_pdf"]})
    if event == "-PDF_PATH-":
        update_values(window=window,key="-SEPERATE_PATH-",args={"value":get_values("-PDF_PATH-")})
    if event == "-PDF_SELECTION-":
        js_bridge["selected_pdf"] = get_values(window=window,st=event)[0]
        update_values(window=window,key="-PDF_PATH-",args={"value":os.path.join(get_values(window=window,st="-PDF_INPUT_LOCATION-"), js_bridge["selected_pdf"])})
        update_values(window=window,key="-SEPERATE_PATH-",args={"value":get_directory(os.path.join(get_values(window=window,st="-PDF_INPUT_LOCATION-"), js_bridge["selected_pdf"]))})
        update_values(window=window,key="-PAGE_START-",args={"value":0})
        update_values(window=window,key="-PAGE_END-",args={"value":get_pdf_pages(os.path.join(get_values(window=window,st="-PDF_INPUT_LOCATION-"),js_bridge["selected_pdf"]))})
    if event == "-SEPARATE_BUTTON-":
        separate_button_action(window)
    if event == "-COLLATE_FOLDER-":
        selected_collate_folder = get_values("-COLLATE_FOLDER-")
        pdf_files_in_folder = get_pdfs_in_directory(selected_collate_folder)
        update_values(window=window,key="-COLLATE_PDF_LIST-",args={"value":pdf_files_in_folder})
    if event == "-COLLATE_BUTTON-":
        collate_button_action(window)
pdf_selector = [[
    get_gui_fun('Frame',{"title":"pdf_files","layout":[[
    get_gui_fun('Listbox',{"values":[],"enable_events":True,"key":"-PDF_SELECTION-","size":(30,10)})]]})]]
choose_pdf_location = [[
    get_gui_fun("Input",{"key":"-PDF_PATH-","enable_events":True}),
    get_gui_fun("FolderBrowse",{"key":"-PDF_INPUT_LOCATION-","enable_events":True})]]
test_button =get_gui_fun('Button',{"button_text":"Generate List","key":"-LIST_BUTTON-","enable_events":True})
collate_button =get_gui_fun('Button', {"button_text": "Collate", "key": "-COLLATE_BUTTON-", "enable_events": True})
collate = [[
    get_gui_fun('Frame',{"title":"collate","layout":[[
        get_gui_fun('Button',{"button_text":"separate","key":"-SEPARATE_BUTTON-","enable_events":True}),
        get_gui_fun("Input",{"key":"-SEPERATE_PATH-","enable_events":True}),
        get_gui_fun("FolderBrowse",{"key":"-PDF_SEPARATE_LOCATION-","enable_events":True}),
        ],[get_gui_fun("T",{"text":"separate folder name"}),get_gui_fun("Input",{"key":"-SEPERATE_FOLDER_NAME-","enable_events":True})]]})]]            
layout = [[test_button,get_page_selection_section()],choose_pdf_location,[pdf_selector],collate]
window = window_mgr.get_new_window("PDF Manipulator",args={"layout":layout,**expandable(),"event_function":"while_events"})
window_mgr.while_basic(window=window)
window.close()
#{"-PDF_INPUT_LOCATION-": {"type": "get","name": "folder_select","args": {"path":{"type": "get","name": "get_value","args": {"st": "-PDF_INPUT_LOCATION-"}}}}})
