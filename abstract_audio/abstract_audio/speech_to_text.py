#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import speech_recognition as sr
from functions import pen, reader_make,reader
from envy_it import *
import subprocess
import PySimpleGUI as sg
import threading
import simpler
# Import the required module for text 
# to speech conversion
# This module is imported so that we can 
# play the converted audio
def pass_text_to_engine(text:str=simpler.main(), lang:str='en', slow:bool=False):
    from gtts import gTTS
    # Language in which you want to convert
    # The text that you want to convert to audio
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    return gTTS(text=mytext, lang=language, slow=False)
def save_audio(file_name:str="welcome.mp3"):
    # Saving the converted audio in a mp3 file named
    # welcome
    pass_text_to_engine().save(file_name)
    # Playing the converted file
    os.system("mpg321 welcome.mp3")
def play_sound(file_name:str="welcome.mp3"):
    from playsound import playsound
    if is_file(file_name):
        playsound(file_name)
load_api_key()
def change_glob(x, y):
    globals()[x] = y
    return y
def get_globe(x):
    if x in globals():
        return globals()[x]
    return ''
def cmd_it(st):
    return subprocess.Popen(st, stdout=subprocess.PIPE, shell=True)
def get_output(p):
    return p.communicate()
def mic_switch():
    return str(get_cmd_out("amixer set Capture toggle")[0])
def get_cmd_out(st):
    return get_output(cmd_it(st))
def parse_mic_state(st: str):
    return str(st).split('[')[-1].split(']')[0]
def get_mic_state():
    return parse_mic_state(get_cmd_out("amixer"))
def win_update(win=get_globe('window'), st:str='-OUTPUT-', data:str =reader_make(filepath='voice.txt') + '\n' + get_globe('voice')):
    try:
        win[st].update(value=data)
    except:
        print('updating',' ',st,' with ',str(data),' didnt work')
def get_values(st):
    if st in get_globe('values'):
        return get_globe('values')[st]
    return None
def save_voice(voice):
    win_update(win=get_globe('window'), st='-OUTPUT-', data=pen(filepath='voice.txt', contents=get_values('-OUTPUT-') + '\n' + change_glob('voice',str(voice))))
def clear_voice():
    win_update(win=get_globe('window'), st='-OUTPUT-', data=pen(filepath='voice.txt', contents=''))
def edit_voice():
    win_update(win=get_globe('window'), st='-OUTPUT-', data=pen(filepath='voice.txt', contents=get_values('-OUTPUT-')))

def playback():
    # instead of updating the GUI directly, put a custom event in the event queue
    try:
        if get_globe('window'):  # Check if window is not None
            get_globe('window').write_event_value('-UPDATE_SCREEN_TEXT-', "processing audio to text")
    except:
        print('updating',' ','-UPDATE_SCREEN_TEXT-',' with ',str("processing audio to text"),' didnt work')

    voice_value = recognzer()
    if str is bytes:  # this version of Python uses bytes for strings (Python 2)
        voice = change_glob('voice', u"{}".format(voice_value).encode("utf-8"))
    else:  # this version of Python uses unicode for strings (Python 3+)
        voice = change_glob('voice', "{}".format(voice_value))
    save_voice(voice)
def start_recording_threaded():
    threading.Thread(target=start_recording).start()
def ambient_noise():
    r.adjust_for_ambient_noise(source)
    window['-SCREEN_TEXT-'].Update(value="Callibrating...\nSet minimum energy threshold to {}".format(r.energy_threshold))
def listen_audio():
    window['-SCREEN_TEXT-'].Update(value="Say something!")
    change_glob('audio', None)  # Initialize audio as None
    while not get_globe('audio'):  # Loop until audio is received or recording is stopped
        try:
            change_glob('audio', r.listen(source, timeout=5))  # Increase timeout if needed
        except Exception as e:
            print(e)
            if not recording:  # If recording has been stopped, break the loop
                change_glob('silence_kill',True)
                break
def recognzer():
    return change_glob('voice_value', r.recognize(audio))
def start_recording():
    change_glob('recording',True)
    try:
        with m as source:
            change_glob('source', source)
            ambient_noise()
            while recording:  # Loop will continue while recording flag is True
                window.Element('-OUTPUT-').Update(background_color='green')
                listen_audio()
                try:
                    if not playback():
                        break
                except LookupError:
                    print("Oops! Didn't catch that")
    except KeyboardInterrupt:
        pass

def record_hit(bool_it):
    if (get_mic_state() == 'off' and bool_it == True) or (get_mic_state() == 'on' and bool_it == False):
        mic_switch()
def stop_record(window=get_globe('window')):
    change_glob('recording',False) 
    window.Element('-OUTPUT-').Update(background_color='white')  # Change color back
    record_hit(False)
    record_hit(True)
    win_update(win=window,data=reader('voice.txt'),st='-OUTPUT-')
    window.Element('-RECORD_BUTTON-').Update(text='record')
    window.Element('-RECORD_BUTTON-').Update(button_color='green')
    window.Element('-STOP_RECORDING-').Update(visible=False)
def recording_true():
    change_glob('recording',True)
def record_button(window=get_globe('window')):
    window.Element('-RECORD_BUTTON-').Update(text='RECORDING')
    window.Element('-RECORD_BUTTON-').Update(button_color='red')
    window.Element('-STOP_RECORDING-').Update(visible=True)
    record_hit(True)
    win_update(win=window,data=reader('voice.txt'),st='-OUTPUT-')
    event ='-RECORD_BUTTON_ACTIVE-'
    window.Element('-RECORD_BUTTON-').Update(button_color='red')
# More of your functions here...

def start_recording():
    change_glob('recording',True)
    try:
        with m as source:
            change_glob('source', source)
            ambient_noise()
            while get_globe('recording'):  # Loop will continue while recording flag is True
                window.Element('-OUTPUT-').Update(background_color='green')
                listen_audio()
                try:
                    playback()
                except LookupError:
                    print("Oops! Didn't catch that")
    except KeyboardInterrupt:
        pass
    finally:
        change_glob('recording', False)  # Reset recording flag at the end

# More of your functions here...

def stop_record(window=get_globe('window')):
    change_glob('recording',False) 
    window.Element('-OUTPUT-').Update(background_color='white')  # Change color back
    record_hit(False)
    record_hit(True)
    win_update(win=window,data=reader('voice.txt'),st='-OUTPUT-')
    window.Element('-RECORD_BUTTON-').Update(text='record')
    window.Element('-RECORD_BUTTON-').Update(button_color='green')
    window.Element('-STOP_RECORDING-').Update(visible=False)

# More of your functions here...

def gui():
    pen(filepath='voice.txt', contents='')
    global recording  # Define a global flag to control recording
    change_glob('recording',False)
    layout = [
        [sg.Multiline('', key='-OUTPUT-', size=(50, 20))],
        [[sg.Button(button_text='record', key='-RECORD_BUTTON-',visible=True,enable_events=True,button_color='green'), sg.Button('STOP',key='-STOP_RECORDING-',visible=False, enable_events=True),sg.Button("-SUBMIT-")],sg.Text('when the screen turns green, speak',key='-SCREEN_TEXT-')]
    ]
    window = sg.Window('Chat', layout)
    change_glob('window', window)
    while True:
        event, values = window.read(timeout=10000)
        change_glob('events',event)
        change_glob('values', values)
        if event == '-UPDATE_SCREEN_TEXT-':
        # now you can safely update the GUI
          window['-SCREEN_TEXT-'].update(value=values[event])
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        if event == '-RECORD_BUTTON-':
            recording_true()
            record_button(window=window)
            start_recording_threaded()
        if event == '-STOP_RECORDING-':
            stop_record(window)
        if event == '-CLEAR_TEXT-':
            clear_voice()
        if event == '-EDIT_TEXT-':
            edit_voice()
        if silence_kill == True:
            change_glob('silence_kill',False)
            stop_record(window = window)
            recording_true()
            record_button(window=window)
        if event == "-SUBMIT-":
            voice = get_values('-OUTPUT-')
            break
            
    window.close()
    return voice

def main():
    change_glob('r', sr.Recognizer())
    change_glob('m', sr.Microphone())
    change_glob('voice', '')
    change_glob('voice_value', '')
    pen(filepath='voice.txt', contents='')
    change_glob('silence_kill',False)
    change_glob('recording',False)
    change_glob('window', '')
    return gui()


