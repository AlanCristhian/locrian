"""GUI widgets of the application."""

import pathlib
import sys
import time
import tkinter

import sound


if sys.platform == "win32":
    try:
        import ctypes
        PROCESS_SYSTEM_DPI_AWARE = 1
        shcore = ctypes.OleDLL("shcore")
        shcore.SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
    except (ImportError, AttributeError, OSError):
        pass


BASE = pathlib.Path()
DELAY = 5
KEYSIM = ("less", "z", "x", "c", "v", "b", "n", "m", "comma", "period",
          "minus", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ntilde",
          "braceleft", "braceright", "Tab", "q", "w", "e", "r", "t", "y", "u",
          "i", "o", "p", "Multi_key", "plus", "bar", "1", "2", "3", "4", "5",
          "6", "7", "8", "9", "0", "quoteright", "questiondown", "BackSpace")


class KeysHandler:
    def __init__(self):
        super().__init__()
        self.bind("<FocusOut>", self.focus_out)
        self.sound = {k: sound.Load(BASE/"g800"/f"{r:02}.mp3")
                      for r, k in zip(range(23, 73), KEYSIM)}
        self.fading = {}
        self.key_press = {}
        self.key_release = {}
        self.pressed = set()
        for key in KEYSIM:
            self.bind_key_press(key)
            self.bind_key_release(key)
        self.after(DELAY, self.fade_out, round(time.monotonic()))

    def fade_out(self, then):
        actual = round(time.monotonic())
        self.after(DELAY - actual + then, self.fade_out, actual)
        sounds = tuple(self.fading.items())
        for key, sound in sounds:
            volume = sound.volume - 100
            if volume > 0:
                sound.volume = volume
            else:
                sound.stop()
                del self.fading[key]

    def bind_key_press(self, keysym):
        sound = self.sound[keysym]
        def key_press(event=None):
            if keysym not in self.pressed:
                if keysym in self.fading:
                    del self.fading[keysym]
                sound.play()
                sound.volume = 1000
                self.pressed.add(keysym)
        self.bind(f"<KeyPress-{keysym}>", key_press)
        self.key_press[keysym] = key_press

    def bind_key_release(self, keysym):
        sound = self.sound[keysym]
        def key_release(event=None):
            if keysym in self.pressed:
                self.pressed.remove(keysym)
                self.fading[keysym] = sound
        self.bind(f"<KeyRelease-{keysym}>", key_release)
        self.key_release[keysym] = key_release

    def focus_out(self, event):
        if event.widget == self:
            for keysym in list(self.pressed):
                self.pressed.remove(keysym)
                self.fading[keysym] = self.sound[keysym]

    def destroy(self):
        try:
            for sound in self.sound.values():
                sound.close()
        finally:
            super().destroy()


class Main(KeysHandler, tkinter.Tk):
    """The main class that load all widgets."""


if __name__ == "__main__":
    Main().mainloop()
