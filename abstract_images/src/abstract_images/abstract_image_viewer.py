import os
import json
import webbrowser
from abstract_gui import get_gui_fun,expandable,create_row_of_buttons
from abstract_utilities.string_clean import eatAll
from abstract_utilities.path_utils import is_file
from abstract_utilities.read_write_utils import read_from_file, write_to_file
from abstract_utilities.compare_utils import get_lower
from abstract_utilities.type_utils import ensure_integer
from .image_utils import read_image,get_image_bytes,resize_image,cv2_image_to_bytesio,image_to_bytes,save_url_img
def change_image_num(k:int=1):
    if k == 1:
        js_bridge["image_num"]+=k
    elif k == -1:
        js_bridge["image_num"]+=k
    if js_bridge["image_num"] <0:
        js_bridge["image_num"] = 0
    elif js_bridge["image_num"] > len(js_bridge["all_list"])-1:
        js_bridge["image_num"] = len(js_bridge["all_list"])-1
    return js_bridge["image_num"]
def event_while(event):
    print(event)
    if js_bridge["all_list"][js_bridge["image_num"]]['title'] in js_bridge["nono_list"]["opened"]:
            window_mgr.update_values(key="Download",args={"disabled":True})
    else:
        window_mgr.update_values(key="Download",args={"disabled":False})
    if event == "grave:49":
        window_mgr.update_values(key="-FRAME_INPUT-",value=0)
    if event == "space:65":
        event = "Download"
    if event == "Shift_L:50":
        event = "skip"
    if event in "1:10,2:11,3:12,4:13,5:14,6:15,7:16,8:17,9:18,0:19".split(','):
        num = int(str(window_mgr.get_values(window_mgr.get_last_window_method())["-FRAME_INPUT-"])+str(event.split(':')[0]))
               
    if event in ['Left:113']:
        event = "Previous"
    elif event in ['Right:114']:
        event = "Next"

    if event in ["-FRAME_INPUT-","Download","Open Image","Previous","Next","Favorite","Remove","skip"]:
        if event == "Previous":
            change_image_num(k=-1)
        if event == "Next":
            change_image_num(k=1)
        if event == "-FRAME_INPUT-":
            val = ensure_integer(window_mgr.get_values()["-FRAME_INPUT-"],len(js_bridge["all_list"])-1)
            window_mgr.update_values(key="-FRAME_INPUT-",value=val)
            if val > len(js_bridge["all_list"])-1:
                window_mgr.update_values(key="-FRAME_INPUT-",value=len(js_bridge["all_list"])-1)
            if val < 0:
                window_mgr.update_values(key="-FRAME_INPUT-",value=0)
        if event == "Open Image":
            webbrowser.open(js_bridge["all_list"][js_bridge["image_num"]]["image"], new=2)
        if event == "skip":
            js_bridge["image_num"] = int(window_mgr.get_values(window_mgr.get_last_window_method())["-FRAME_INPUT-"])
        if event == "Download":
            if js_bridge["all_list"][js_bridge["image_num"]]['title'] not in js_bridge["nono_list"]["opened"]:
                webbrowser.open(js_bridge["all_list"][js_bridge["image_num"]]["download"], new=2)
                js_bridge["nono_list"]["opened"].append(js_bridge["all_list"][js_bridge["image_num"]]['title'])
            write_to_file(filepath="/home/john-putkey/Documents/python_projects/zip_never_list_2.py",contents=json.dumps(js_bridge["nono_list"]))
            change_image_num(k=1)
        
        if event in ["skip","Next","Previous","Download"]:
            try:
                window_mgr.update_values(key="-CURR_IMG-",args={"value":js_bridge["image_num"]})
                window_mgr.update_values(key="-IMAGE_TITLE-",args={"value":js_bridge["all_list"][js_bridge["image_num"]]["title"]})
                window_mgr.update_values(key="-IMAGE_AUTHOR-",args={"value":js_bridge["all_list"][js_bridge["image_num"]]["user"]})
                window_mgr.update_values(key="-IMAGE_PATH-",args={"value":js_bridge["all_list"][js_bridge["image_num"]]["download"]})
                window_mgr.update_values(key="-IMAGE_COMPONENT-", args={"data": resize_image(image_path=os.path.join("/home/john-putkey/Documents/python_projects",js_bridge["all_list"][js_bridge["image_num"]]["save_image"]), max_width=1000, max_height=800)})
            except Exception as e:
                print(f"shit didnt work: {e}")
def abstract_image_viewer_main(all_list_directory,nono_list_directory):
    window_mgr,upload_bridge,script_name=create_window_manager(global_var=globals())
    js_bridge = upload_bridge.return_global_variables(script_name=script_name)
    js_bridge["image_num"] = 0
    js_bridge["all_list"]=json.loads(read_from_file(all_list_directory))
    js_bridge["nono_list"]=json.loads(read_from_file(nono_list_directory))
    image_path =os.path.join(js_bridge["all_list"][0]["save_image"])
    layout = [[[[get_gui_fun("T",args={"text":"title","key":"-IMAGE_TITLE-"})],
        [get_gui_fun("T",args={"text":"author","key":"-IMAGE_AUTHOR-"})],
        [get_gui_fun("T",args={"text":"title","key":"-IMAGE_PATH-"})],
        [get_gui_fun("T",args={"text":"0","key":"-CURR_IMG-"}),get_gui_fun("T",args={"text":"of"}),get_gui_fun("T",args={"text":len(js_bridge["all_list"]),"key":"-MAX_IMG-"})]],
        [get_gui_fun("Image",args={"data":resize_image(image_path, max_width=800, max_height=450),"size":(None,None),"key":"-IMAGE_COMPONENT-"})],
        [create_row_of_buttons("Download","Open Image","Previous","Next","Favorite","Remove"),get_gui_fun("Frame",args={"title":"","layout":
                                   [[get_gui_fun("Input",args={"default_text":0,"size":(6,2),"key":"-FRAME_INPUT-","enable_events":True})]]})],create_row_of_buttons("skip"),]]
    window = window_mgr.get_new_window("Abstract Image Viewer",args={"layout":layout,"size": (1200,1600),"event_function":"event_while",**expandable(),"return_keyboard_events":True})
    window_mgr.while_basic(window=window)

