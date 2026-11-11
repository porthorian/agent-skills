import unittest
from unittest.mock import patch

import notifier


class NotifyTests(unittest.TestCase):
    def test_appends_to_supplied_history(self):
        history = ["earlier"]
        with patch("notifier.send", return_value="receipt"):
            self.assertEqual(notifier.notify("a@example.test", history), ["earlier", "receipt"])


if __name__ == "__main__":
    unittest.main()
