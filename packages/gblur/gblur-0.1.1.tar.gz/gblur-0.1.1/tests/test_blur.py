#!/usr/env/bin python3

from unittest import TestCase, main
import gblur

class TestBlur(TestCase):
    def setUp(self):
        self.radius = 1
    def test_blur(self):
        f = open("tests/cballs.png", "rb")
        buf = f.read()
        f.close()
        img = gblur.blur(buf, self.radius)
        f = open("tests/cballs_blurred.png", "rb")
        good = f.read()
        self.assertEqual(bytearray(img), good)
        f.close()

if __name__ == '__main__':
    main()
