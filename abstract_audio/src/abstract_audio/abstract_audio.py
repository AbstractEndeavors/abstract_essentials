from audio_player.__init__ import AudioPlayer
import platform
import subprocess
import os
import pydub
from pydub import AudioSegment

class WindowsVolumeCommands:
    def __init__(self):
        self.max_volume = 65535
        self.operating_system=get_os_info()['operating_system']
        self.os_bit_size=get_os_info()['bit_size']
        self.os_sound_directory = self.os_bit_type_directory()
        self.sound_dir_json = self.get_sound_mixer_directory()
    def os_bit_type_directory(self):
        os_info = get_os_info()
        bit_type_directory = os.path.join(
            os.getcwd(),
            'volume_states',
            self.operating_system,
            self.os_bit_size
            )
        return bit_type_directory
    def get_sound_mixer_directory(self):
        sound_directories = get_dirs(self.os_sound_directory)
        sound_dir_json={}
        for each in sound_directories:
            if 'nircmd' in each:
                sound_dir_json["nircmd"]=os.path.join(self.os_sound_directory,each)
            if 'svcl' in each:
                sound_dir_json["svcl"]=os.path.join(self.os_sound_directory,each)
        return sound_dir_json
    def execute_volume_mixer_cmd(self,mixer,arg):
        return cmd_it(f'cd {self.sound_dir_json[mixer]} & {mixer}.exe '+arg)
    def toggle_mute_system(self):
        return self.execute_volume_mixer_cmd('nircmd','mutesysvolume 2')
    def mute_system(self):
        return self.execute_volume_mixer_cmd('nircmd','mutesysvolume 1')
    def unmute_system(self):
        return self.execute_volume_mixer_cmd('nircmd','mutesysvolume 0')
    def check_volume(self):
        result = self.execute_volume_mixer_cmd('svcl','/Stdout /GetPercent "Speakers"')
        return get_output(result)
    def set_volume(self,incriment:(int or float)=0):
        if type_compare(incriment,float):
            new_volume = str(self.max_volume*incriment)
        else:
            new_volume = str(incriment)
        return self.execute_volume_mixer_cmd('nircmd',f'setsysvolume {new_volume}')
    def change_volume(self, incriment: (int, float) = 0):
        volume_output = self.check_volume().strip()  # Remove leading/trailing whitespace
        if type_compare(incriment, float):
            new_volume = int(float(volume_output) * float(incriment))
        else:
            new_volume = int(float(volume_output) + float(incriment))
        return self.execute_volume_mixer_cmd('nircmd', f'setsysvolume {new_volume}')
class Player:
    def __init__(self, filepath):
        self.filepath = filepath
        self.audio = AudioSegment.from_file(self.filepath)
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
        AudioPlayer(self.filepath).play(block=True)
        #self.play_obj = sa.play_buffer(raw_data, num_channels, sample_width, frame_rate)
        #self.start_time = time.time()

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
globals()["audio_file"]='test_audio/c.wav'
audio_player = Player(audio_file).play_audio()
audio_object = AudioSegment.from_file(audio_file)
audio_object_length = len(audio_object)
AudioPlayer(audio_file).play(block=True)
first_half = audio_object[:int(audio_object_length/2)]
first_half.export("first_half.wav", format="wav")
AudioPlayer("first_half.wav").play(block=True)
second_half = audio_object[audio_object_length/2:]
second_half.export("second_half.wav", format="wav")
AudioPlayer("second_half.wav").play(block=True)


def get_os_info():
    os_name = platform.system()
    bit_size = platform.architecture()[0]
    return {"operating_system": os_name, "bit_size": bit_size}
def get_output(result):
    stdout, _ = result.communicate()
    return stdout
def cmd_it(st):
    return subprocess.Popen(st, stdout=subprocess.PIPE, shell=True, text=True)
def type_compare(var:object,class_info:type):
    if class_info != type:
        if type(class_info) == object: 
            class_info = type(class_info)
    return isinstance(var, class_info)
def get_dirs(path):
    from os import walk
    for (dirpath, dirnames, filenames) in walk(path):
        return dirnames
volume_control=WindowsVolumeCommands()
volume_control.change_volume(100)
