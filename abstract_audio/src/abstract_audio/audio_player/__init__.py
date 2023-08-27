from platform import system
if system() == 'Windows':
    from .audioplayer_windows import AudioPlayerWindows as AudioPlayer
elif system() == 'Darwin':
    from .audioplayer_macos import AudioPlayerMacOS as AudioPlayer
else:
    from .audioplayer_linux import AudioPlayerLinux as AudioPlayer
