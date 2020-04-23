"""A little improvement over playsound. Use uuid4 for alias"""


from ctypes import c_buffer, windll
from sys    import getfilesystemencoding
from uuid   import uuid4
from itertools import cycle


__all__ = ["Load"]


_mciSendStringA = windll.winmm.mciSendStringA
_mciGetErrorStringA = windll.winmm.mciGetErrorStringA
_waveOutSetVolume = windll.winmm.waveOutSetVolume


SYSTEM_ENCODING = getfilesystemencoding()
CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
LEN_CHARS = len(CHARS)


# Represent an integer as alphanumeric.
def _int_to_alpha(i: int):
    s = ""
    while i:
        s += CHARS[i % LEN_CHARS]
        i //= LEN_CHARS
    return s


# Execute an MCI command
def _mci_command(command):
    command = command.encode(SYSTEM_ENCODING)
    buffer = c_buffer(255)
    error_code = int(_mciSendStringA(command, buffer, 254, 0))
    if error_code:
        _mciGetErrorStringA(error_code, buffer, 254)
        error_message = (f"\n    Error {error_code} for command:"
                         f"\n        {command.decode('utf-8')}"
                         f"\n    {buffer.value.decode('unicode_escape')}")
        raise RuntimeError(error_message)
    return buffer.value


class Load:
    """
    Open a sound file.

    :param path.Path path: path of the mp3 file
    """

    def __init__(self, path):
        self.is_open = False
        aid = _int_to_alpha(uuid4().int)
        alias = f"key_{aid}"
        self._close = f"close {alias}"
        self._mode = f"status {alias} mode"
        self._play = f"play {alias} from 95"
        self._set_volume = f"setaudio {alias} volume to %d"
        self._get_volume = f"status {alias} volume"
        self._stop = f"stop {alias}"
        _mci_command(f'open "{path}" alias {alias}')
        self.is_open = True
        _mci_command(f"set {alias} time format milliseconds")
        _mci_command(f"cue {alias} output")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self.is_open:
            _mci_command(self._close)
            self.is_open = False

    @property
    def is_playing(self):
        """Returns ``True`` if the file is playing, ``False`` otherwise."""
        if _mci_command(self._mode) == b"playing":
            return True
        return False

    def play(self):
        """Starts playing the sound."""
        _mci_command(self._play)

    @property
    def volume(self):
        """Get the actual volume of the first instance of the sound."""
        return int(_mci_command(self._get_volume))

    @volume.setter
    def volume(self, value):
        """Set the volume of the first instance of the sound."""
        _mci_command(self._set_volume % value)

    def stop(self):
        _mci_command(self._stop)
