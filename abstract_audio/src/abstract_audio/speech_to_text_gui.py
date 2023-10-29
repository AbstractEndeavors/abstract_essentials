#!/usr/bin/env python3
import os
import subprocess
import threading
import speech_recognition as sr
from abstract_utilities.read_write_utils import write_to_file, create_and_read_file,read_from_file
from abstract_gui import *
"""
This module provides functionalities to capture and manipulate audio input 
from a microphone and save them into a text file. It uses an abstract GUI 
to display the state of audio recording and playback.

The main functions in this script are as follows:
- change_glob: A utility function to update and retrieve global variables dynamically.
- get_globe: A utility function to retrieve the value of a global variable if it exists.
- cmd_it: Executes a shell command using subprocess and returns a Popen object for communication.
- get_output: Retrieves the output of a subprocess Popen object.
- mic_switch: Toggles the microphone state between on and off using the 'amixer set Capture toggle' command.
- parse_mic_state: Parses the microphone state from the output of 'amixer' command.
- get_mic_state: Retrieves the current microphone state.
- win_update: Updates the GUI window with new values for a given key.
- get_cmd_out: Executes a shell command and returns its output.
- get_values: Retrieves a value from the GUI window's stored values using the given key.
- save_voice: Saves the voice recording to a file 'voice.txt' and updates the GUI window accordingly.
- playback: Starts the speech recognition process and updates the GUI window with the recognized text.
- start_recording_threaded: Starts the recording process in a separate thread to avoid blocking the GUI.
- ambient_noise: Adjusts for ambient noise before starting the actual audio recording.
- listen_audio: Listens for audio input and stores it in the global variable 'audio'.
- recognzer: Uses the Google Web Speech API to recognize the audio and store the result in 'voice_value'.
- start_recording: Starts the audio recording process and handles exceptions for KeyboardInterrupt.
- get_gui_layout: Defines the layout for the PySimpleGUI GUI window.
- voice_record_function: Handles different events triggered by the GUI window and performs corresponding actions.
- gui: Initializes the GUI window, sets global variables, and starts the main GUI event loop.
- main: Sets up global variables, initializes the SpeechRecognizer and Microphone objects, and starts the GUI.

To use this script, run it as a Python program. It will open a GUI window with a 'record' button. Clicking on the 'record' button will start the audio recording, and the GUI screen will turn green to indicate recording. Once you stop speaking, the recorded audio will be processed using the Google Web Speech API, and the recognized text will be displayed in the GUI window.

Note: To use this script, make sure to have the required libraries installed, such as PySimpleGUI and SpeechRecognition.

Author: putkoff
Date: 8/1/23
"""
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
def parse_mic_state(st: str):
    return str(st).split('[')[-1].split(']')[0]
def get_mic_state():
    return parse_mic_state(get_cmd_out("amixer"))
def win_update(win=get_globe('window'), st:str='-OUTPUT-', data:str =create_and_read_file(file_path='voice.txt') + '\n' + get_globe('voice')):
    try:
        window_mgr.update_values(window=win,key=st,value=data)
    except:
        print('updating',' ',st,' with ',str(data),' didnt work')
def get_cmd_out(st):
    return get_output(cmd_it(st))
def get_values(st):
    if st in window_mgr.get_values():
        return window_mgr.get_values()[st]
    return None
def save_voice(voice):
    text_value = read_from_file(file_path='voice.txt') + '\n' + change_glob('voice',str(voice))
    write_to_file(file_path='voice.txt', contents=text_value)
    win_update(win=get_globe('window'),st='-OUTPUT-', data=text_value)
def playback():
    # instead of updating the GUI directly, put a custom event in the event queue
    try:
        if get_globe('window'):  # Check if window is not None
            win_update(win=get_globe('window'), st="-SCREEN_TEXT-", data="processing audio to text")
    except:
        print('updating',' ','-UPDATE_SCREEN_TEXT-',' with ',str("processing audio to text"),' didnt work')

    recognzer()
    if voice_value != None:
        if str is bytes:  # this version of Python uses bytes for strings (Python 2)
            voice = change_glob('voice', u"{}".format(voice_value).encode("utf-8"))
        else:  # this version of Python uses unicode for strings (Python 3+)
            voice = change_glob('voice', "{}".format(voice_value))
        save_voice(voice)
def start_recording_threaded():
    threading.Thread(target=start_recording).start()
def ambient_noise():
    r.adjust_for_ambient_noise(source)
    win_update(win=get_globe('window'),st='-SCREEN_TEXT-',data="Callibrating...\nSet minimum energy threshold to {}".format(r.energy_threshold))
def listen_audio():
    win_update(win=get_globe('window'),st='-SCREEN_TEXT-',data="Say something!")
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
    try:
        new_value = r.recognize_google(audio)
        change_glob('voice_value',new_value)
    except:
        win_update(win=get_globe('window'),st='-SCREEN_TEXT-',data="looks like we didnt catch that, could you please repeat it?")
        change_glob('voice_value',None)
 
def start_recording():
    change_glob('recording',True)
    try:
        with m as source:
            change_glob('source', source)
            ambient_noise()
            while recording:  # Loop will continue while recording flag is True
                get_globe('window').Element('-OUTPUT-').Update(background_color='green')
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
    win_update(win=window,data=read_from_file('voice.txt'),st='-OUTPUT-')
    window.Element('-RECORD_BUTTON-').Update(text='record',button_color='green')
    window.Element('-STOP_RECORDING-').Update(visible=False)
def recording_true():
    change_glob('recording',True)
def record_button(window=get_globe('window')):
    window.Element('-RECORD_BUTTON-').Update(text='RECORDING',button_color='red')
    window.Element('-STOP_RECORDING-').Update(visible=True)
    record_hit(True)
    win_update(win=window,data=read_from_file('voice.txt'),st='-OUTPUT-')
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
def get_gui_layout():
    return[
        [
            sg.Multiline('', key='-OUTPUT-', size=(50, 20),enable_events=True)],
        [
            [
                sg.Button(button_text='record', key='-RECORD_BUTTON-',visible=True,enable_events=True,button_color='green'),
                sg.Button('STOP',key='-STOP_RECORDING-',visible=False, enable_events=True),
                sg.Button("-SUBMIT-")
                ],
            sg.Text('when the screen turns green, speak',key='-SCREEN_TEXT-')
            ]
        ]
def voice_record_function(event):
    global edit_timer  # To access the timer variable

    if event == '-UPDATE_SCREEN_TEXT-':
        win_update(win=window, st='-SCREEN_TEXT-', data=window_mgr.get_values()[event])
        # Reset the edit_timer on each edit event
        if edit_timer:
            edit_timer.Stop()
        edit_timer = window_mgr.window.set_timeout(100, 'pause_timeout')

    elif event == '-RECORD_BUTTON-':
        recording_true()
        record_button(window=window)
        start_recording_threaded()

    elif event == '-STOP_RECORDING-':
        stop_record(window)

    elif event == '-OUTPUT-':
        # The user is editing the content, save the current content to a temporary file
        temp_file = 'voice_edit.txt'
        if os.path.exists('voice_edit.txt')==False:
            write_to_file(file_path=temp_file, contents=read_from_file(file_path='voice.txt'))
            write_to_file(file_path='voice.txt', contents='')
        write_to_file(file_path=temp_file, contents=window_mgr.get_values()[event])
        print(window_mgr.get_values()[event])
        if os.path.exists('voice_edit.txt'):
            edited_content = window_mgr.get_values()[event]
            write_to_file(file_path='voice.txt', contents=read_from_file('voice_edit.txt') + read_from_file('voice.txt'))
            os.remove('voice_edit.txt')  # Remove the temporary file
            # Update the '-OUTPUT-' element with the combined content
        
    elif event == 'pause_timeout':
        # Timeout event indicates a pause in editing, update the content and remove temporary file
        if os.path.exists('voice_edit.txt'):
            win_update(win=window, st='-OUTPUT-', data=read_from_file('voice.txt'))
            os.remove('voice_edit.txt')  # Remove the temporary file
def gui():
    write_to_file(file_path='voice.txt', contents='')
    global recording  # Define a global flag to control recording
    change_glob('recording',False)
    change_glob('window',window_mgr.get_new_window(title='speech_to_text_window', layout=get_gui_layout(), event_function="voice_record_function", exit_events=['Quit',"-SUBMIT-"]))
    return window_mgr.while_basic(window=window)
def main():
    change_glob('r', sr.Recognizer())
    change_glob('m', sr.Microphone())
    change_glob('voice', '')
    change_glob('voice_value', '')
    write_to_file(file_path='voice.txt', contents='')
    change_glob('silence_kill',False)
    change_glob('recording',False)
    
    return gui()
window_mgr,bridge,script_name = abstract_gui.create_window_manager(script_name="speech_to_text",global_var=globals())


