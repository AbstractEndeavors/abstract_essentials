import PySimpleGUI as sg
from pydub import AudioSegment
import simpleaudio as sa
import time
import threading
import subprocess

def change_globs(x, y):
    globals()[x] = y
def get_duration(filename):
    audio = AudioSegment.from_file(filename)
    duration_in_ms = len(audio)
    duration_in_s = duration_in_ms / 1000  # convert to seconds
    return duration_in_s
def get_output(p):
    return p.communicate()
def volume_toggle(num:int=5):
    return str(get_output(cmd_it(f'amixer -q sset Master {num}%')))
def parse_volume_state(st: str):
    return str(st).split('[')[-2].split(']')[0]
def get_volume_state():
    return parse_volume_state(get_output(cmd_it("amixer sget Master")))
class Player:
    def __init__(self, filepath):
        self.filepath = filepath
        self.audio = AudioSegment.from_file(filepath)
        self.duration = len(self.audio)
        self.play_obj = None
        self.start_time = None
        self.current_position = 0

    def play_audio(self):
        audio_segment = self.audio[self.current_position:]
        raw_data = audio_segment.raw_data
        sample_width = audio_segment.sample_width
        num_channels = audio_segment.channels
        frame_rate = audio_segment.frame_rate

        self.play_obj = sa.play_buffer(raw_data, num_channels, sample_width, frame_rate)
        self.start_time = time.time()

    def stop_audio(self):
        if self.play_obj is not None:
            self.play_obj.stop()
        self.start_time = None

    def pause_audio(self):
        if self.play_obj is not None:
            self.current_position += (time.time() - self.start_time) * 1000
            self.play_obj.stop()
        self.start_time = None

    def get_current_position(self):
        if self.start_time is None:
            return self.current_position
        return self.current_position + (time.time() - self.start_time) * 1000  # ms

change_globs('file_path',"new_audio.mp3")
change_globs('p',Player(file_path))
change_globs('duration',get_duration(file_path))
change_globs('window',None)
change_globs('play',False)
change_globs('pause',False)

layout = [[sg.Text("Audio Player")],
          [[sg.Text('0.00'), sg.ProgressBar(duration, orientation='h', size=(100,20), key='progressbar'), sg.Text(str(duration))],
           [sg.Slider(range=(0, duration), resolution=0.01, default_value=0, size=(100,20), orientation='horizontal', key='position', enable_events=True)]],
          [sg.Slider(range=(1, 22), default_value=1, size=(10, 15), orientation='horizontal', key='speed', enable_events=True)],
          [sg.Button('1x speed',key='speed_button')],
          [sg.Text("Audio Player")],
          [sg.Button('Play'), sg.Button('Stop'), sg.Button('Pause'), sg.Button('Resume')],
          [sg.Text('volume: '), sg.Slider(range=(0, 100), default_value=int(get_volume_state().split('%')[0]), size=(15, 15), orientation='horizontal', key='volume', enable_events=True)],
]
window = sg.Window('Audio Player', layout)
while True:
    event, values = window.read(timeout=100)  # every 100 ms the GUI will update
    change_globs('values',values)
    if event == sg.WINDOW_CLOSED:
        p.stop_audio()
        break
    if event == 'position':
        
        if play:
          play = False
          pause = True
          p.current_position = values['position'] * 1000
          p.pause_audio()
          play = True
          pause = False
          p.play_audio()
        else:
          p.current_position = values['position'] * 1000
          window['progressbar'].UpdateBar(values['position'])
    elif event == 'Play':
        if not play:
          play = True
          pause = False
          p.play_audio()
    elif event == 'Stop':
        play = False
        p.stop_audio()
        p.current_position = 0
        window['progressbar'].UpdateBar(0)
        window['position'].update(value=0)
    elif event == 'Pause':
        play = False
        pause = True
        p.pause_audio()
    elif event == 'Resume':
        if pause:
            play = True
            pause = False
            p.play_audio()
    elif event == 'speed':
        window.Element('speed_button').update(text=f'{values["speed"]}x speed')
    elif event == 'speed_button':
        p.change_speed(float(values["speed"]))
    elif event == 'volume':
        volume_toggle(int(values["volume"]))
    if play:
        pos = p.get_current_position() / 1000
        window['progressbar'].UpdateBar(pos)
        window['position'].update(value=pos)
window.close()
