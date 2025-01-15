import unittest

from pryfixer import main


class TestPryfixer(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
