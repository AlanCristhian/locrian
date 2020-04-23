import pathlib
import unittest
import re

import sound


BASE = pathlib.Path()


class HelpersCase(unittest.TestCase):
    def test_int_to_alpha_function(self):
        self.assertEqual(sound._int_to_alpha(61), "Z")


class LoadCase(unittest.TestCase):
    def test_instance(self):
        with sound.Load(BASE/"g800"/"00.mp3") as s00:
            self.assertIsInstance(s00, sound.Load)
        self.assertFalse(s00.is_open)

    def test__close__attribute(self):
        with sound.Load(BASE/"g800"/"01.mp3") as s01:
            self.assertTrue(s01._close.startswith("close key_"))

    def test_play(self):
        with sound.Load(BASE/"g800"/"02.mp3") as s02:
            self.assertFalse(s02.is_playing)
            s02.play()
            self.assertTrue(s02.is_playing)

    def test_volume(self):
        with sound.Load(BASE/"g800"/"03.mp3") as s03:
            self.assertEqual(s03.volume, 1000)
            s03.volume = 500
            self.assertEqual(s03.volume, 501)

    def test_stop(self):
        with sound.Load(BASE/"g800"/"04.mp3") as s04:
            self.assertFalse(s04.is_playing)
            s04.play()
            self.assertTrue(s04.is_playing)
            s04.stop()
            self.assertFalse(s04.is_playing)


if __name__ == "__main__":
    unittest.main()
