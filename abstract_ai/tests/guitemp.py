import threading
import PySimpleGUI as sg
import inspect
import os

from abstract_utilities.class_utils import call_functions,process_args,get_fun,mk_fun,change_glob
from abstract_utilities.type_utils import is_iterable

def expandable(size:tuple=(None, None)):
    return {"size": size,"resizable": True,"scrollable": True,"auto_size_text": True,"expand_x":True,"expand_y": True}

change_glob(var='all_windows',val={'last_window':{'name':'','values':{},'event':''}},glob=globals())
def get_glob(obj:str='',glob=globals()):
    try:
        return glob[obj]
    except KeyError:
        print(f"No global object named '{obj}'")
        return None
class Event:
    def __init__(self, key, function_name, global_namespace, args):
        self.key = key
        self.function_name = function_name
        self.global_namespace = global_namespace
        self.args = args

    def perform_action(self):
        # fetch the function from the global namespace
        function = self.global_namespace[self.function_name]
        processed_args = self.process_args(self.args)
        function(**processed_args)

    @staticmethod
    def process_args(args):
        # This function processes the arguments similar to your 'process_args' function
        # It could resolve functions specified in the arguments, for example.
        pass

#progress_bars
def update_progress(win:str='progress_window',st:str='bar',progress:(int or float)=0):
    win[st].update_bar(progress)
def get_progress_bar(max_value:int=100, size:tuple=(30,10),key:str='bar'):
    return get_gui_fun('ProgressBar',{"max_value":max_value, "size":size, "key":key})
#windows
def get_window(title:str='basic window',layout:list=[[]]):
    return sg.Window(title, layout)
def verify_window(win:any=None):
  if type(win) == str:
    win = get_glob(obj=win)
  if type(win) == type(get_window()):
    return True
  return False
def close_window(win:any=None):
  if verify_window(win):
    win.close()
#components
def get_gui_fun(name:str='',args:dict={}):
  import PySimpleGUI
  return get_fun({"instance":PySimpleGUI,"name":name,"args":args})
#check_whiles
def win_closed(event:str=''):
    return T_or_F_obj_eq(event=event,obj=sg.WIN_CLOSED)
#check_bools
def T_or_F_obj_eq(event:any='',obj:any=''):
  return True if event == obj else False
def det_bool_T(obj:(tuple or list or bool)=False):
  if isinstance(obj, bool):
    return obj 
  return any(obj)
def det_bool_F(obj:(tuple or list or bool)=False):
  if isinstance(obj, bool):
    return obj
  return all(obj)
#number_verifications
def out_of_bounds(upper:(int or float)=100,lower:(int or float)=0,obj:(int or float)=-1):
  return det_bool_T(obj > 100 or obj < 0)
def create_win_name():
  all_windows = get_glob('all_windows')
  keys = list(all_windows.keys())
  i,curr_try = 'default_window',0
  while curr_try in keys:
    curr_try = f'default_window_{i}'
    i +=1
  return curr_try
#while_windows
def update_read(curr_win:type(get_window()),win_name:str=create_win_name()):
    all_windows = get_glob('all_windows')
    event, values = curr_win.read()
    if win_name not in all_windows:
      all_windows[win_name] = {'event':'','values':{}}
      change_glob(win_name,curr_win)
    all_windows[win_name]['event']=event
    all_windows[win_name]['values']=values
    all_windows['last_window']['name']=win_name
    all_windows['last_window']['event']=event
    all_windows['last_window']['values']=values
    change_glob('all_windows',all_windows)
def get_js_st(js,st):
  if st in js:
    return js[st]
def while_basic_events(event_win:type(get_window())=get_window(),win_name:str=create_win_name(),events:dict={}):
    while verify_window(event_win):
        update_read(curr_win=event_win,win_name='event_win')
        if win_closed(get_event(event_win)):
            break
        keys = list(events.keys())
        for k in range(0,len(keys)):
          key = keys[k]
          if T_or_F_obj_eq(event=get_event(curr_win=win_name),obj=key):
            func_specs = events[key]
            args,instance,function_name = (),None,''
            if is_iterable(func_specs):
                args = process_args(func_specs['args'])
                instance=get_js_st(func_specs,'instance')
                function_name = get_js_st(func_specs,'name')
            call_functions(args=args, instance=instance, function_name=function_name,glob=globals())
    close_window(event_win)
def while_basic(win=None):
    if win is None:
        win = get_glob(obj='window')
    while verify_window(win):
        event, values = win.read()
        if win_closed(event):
            break
    close_window(win)
def get_last_window():
    return get_glob('all_windows')['last_window']['name']
def while_progress(win=None, progress:int=0, step:int=5, thread=None):
    if win is None:
        win = get_last_window()
    while verify_window(win):
      event, values = win.read(timeout=100)
      if win_closed(event) or not thread_alive(thread):
          break
      win.read(timeout=100)
      update_progress(win=win,st='bar',progress=progress)
      progress += step
      if out_of_bounds(upper=100,lower=0,obj=progress):
        step *= -1
    close_window(win)
#values
def update(curr_win:(str or type(get_window()))='last_window',st:str='',obj:any=''):
    all_windows = get_glob('all_windows')
    input([st,all_windows])
    all_windows['last_window'][st].update(values=obj)
    if type(obj) is list:
        all_windows['last_window'][st].update(value=obj[0])
    change_glob('all_windows',all_windows)
def get_value(curr_win:(str or type(get_window()))='last_window',st:str=''):
  all_windows=get_glob('all_windows')
  win_name = curr_win
  if type(curr_win) == type(get_window()):
    update_read(curr_win)
    win_name = 'last_window'
  curr_js = all_windows[curr_win]
  if st in curr_js['values']:
    return curr_js['values'][st]
def get_event(curr_win:(str or type(get_window()))='last_window',st:str=''):
  all_windows=get_glob('all_windows')
  win_name = curr_win
  if type(curr_win) == type(get_window()):
    update_read(curr_win)
    win_name = 'last_window'
  curr_js = all_windows[win_name]
  return curr_js['event']
#threading
def get_thread(target=None,args=(),daemon=True):
    return threading.Thread(target=target, args=args, daemon=daemon)
def start_thread(thread=None):
  if verify_thread(thread):
    thread.start()
def verify_thread(thread=None):
  return T_or_F_obj_eq(type(thread),type(threading.Thread()))
def thread_alive(thread):
  if verify_thread(thread):
    return thread.is_alive()
  return False
#text to audio
def save_audio(text:str='',file_path:str="welcome.mp3"):
  from gtts import gTTS
  myobj = gTTS(text=text, lang='en', slow=False)
  myobj.save(f"{file_path}")
  os.system(f"mpg321 {file_path}")
def play_audio(file_path:str="welcome.mp3"):
  from playsound import playsound
  if os.path.isfile(file_path):
      playsound(file_path)
def save_play_audio(text:str='',file_path:str="welcome.mp3"):
  save_audio(text=text,file_path=file_path)
  thread = threading.Thread(target=play_audio, args=(file_path,))
  thread.start()

#example of simple modularization
while_basic(win=get_gui_fun('Window',{'title':'display',"layout":[[get_gui_fun('Multiline',args={"sdasdfsdf":"","default_text":"hey"})]]}))
#ecample of complex modularization
while_basic_events(
  get_gui_fun('Window',{'title':'chat GPT output', 'layout':[[
    get_gui_fun('T',{'text':'query: '}),
    get_gui_fun('Multiline',{'default_text':'this is a question',**expandable()})],[
      get_gui_fun('T',{'text':'response: '}),
      get_gui_fun('Multiline', {'default_text': 'this is an answer', 'key': "-RESPONSE-",**expandable()}),[
        get_gui_fun('Button', {"button_text": 'Play Audio', "key": '-PLAY_AUDIO-'})]]],**expandable(size=(300,300))}),
  events={'-PLAY_AUDIO-': {"type": "get","global":globals(),"name": "save_play_audio","args": {"text": {"type": "get","global":globals(), "name": "get_value", "args": {"st": "-RESPONSE-"}}, "file_path": "new_audio.mp3"}}}
  )
