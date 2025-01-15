import unittest

from latinUzConverter.core import LatinUzConverter


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.converter = LatinUzConverter()

    def test_to_cyrillic(self):
        self.assertEqual(self.converter.to_cyrillic("Salom"), "Салом")

    def test_to_latin(self):
        self.assertEqual(self.converter.to_latin("Салом"), "Salom")


if __name__ == "__main__":
    unittest.main()
