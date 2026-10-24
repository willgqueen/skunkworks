import unittest

from greet import greet


class Greet(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Ada"), "Hello, Ada!")

    def test_shout(self):
        self.assertEqual(greet("Ada", shout=True), "HELLO, ADA!")


if __name__ == "__main__":
    unittest.main()
