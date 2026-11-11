import unittest

from options import parse_limit, parse_retries


class OptionTests(unittest.TestCase):
    def test_limit_default(self):
        self.assertEqual(parse_limit(None), 100)

    def test_zero_retries(self):
        self.assertEqual(parse_retries("0"), 0)


if __name__ == "__main__":
    unittest.main()
