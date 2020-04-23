import gc
import unittest
import time

import widget


class BaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = widget.Main()
        cls.main.withdraw()
        cls.main.update_idletasks()

    @classmethod
    def tearDownClass(cls):
        cls.main.update_idletasks()
        cls.main.destroy()
        del cls.main
        gc.collect()


class KeyHandlersSuite(BaseCase):
    def test_instance(self):
        self.assertIsInstance(self.main, widget.KeysHandler)

    def test_key_pressed_and_released(self):
        self.assertEqual(len(self.main.pressed), 0)
        self.main.key_press["w"]()
        self.assertEqual(len(self.main.pressed), 1)
        self.main.key_release["w"]()
        self.assertEqual(len(self.main.pressed), 0)

    def test_two_key_pressed_and_released(self):
        self.assertEqual(len(self.main.pressed), 0)
        self.main.key_press["w"]()
        self.main.key_press["e"]()
        self.assertEqual(len(self.main.pressed), 2)
        self.main.key_release["w"]()
        self.assertEqual(len(self.main.pressed), 1)
        self.main.key_release["e"]()
        self.assertEqual(len(self.main.pressed), 0)


class MainSuite(BaseCase):
    def test_instance(self):
        self.assertIsInstance(self.main, widget.Main)


if __name__ == "__main__":
    unittest.main()
