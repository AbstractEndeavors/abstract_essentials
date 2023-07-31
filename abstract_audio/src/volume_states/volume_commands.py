import platform
import subprocess
import os
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
volume_commands = WindowsVolumeCommands()


