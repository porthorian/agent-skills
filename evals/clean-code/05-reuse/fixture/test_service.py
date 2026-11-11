import unittest

from service import create_job, preview_job


class JobTests(unittest.TestCase):
    def test_create_response(self):
        self.assertEqual(create_job("west"), {"region": "west", "preview": False})

    def test_preview_response(self):
        self.assertEqual(preview_job("west"), {"region": "west", "preview": True})


if __name__ == "__main__":
    unittest.main()
