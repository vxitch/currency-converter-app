"""Task 2(a): If the user submits the form with no currency amount,
the app should not crash - it should return a normal page with an error message."""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app


class TestEmptyInput(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_empty_amount_does_not_crash(self):
        """Submitting an empty amount should return HTTP 200, not a 500 crash."""
        response = self.client.post(
            "/",
            data={"amount": "", "from_currency": "USD", "to_currency": "GBP"},
        )
        self.assertEqual(response.status_code, 200)

    def test_empty_amount_shows_error_message(self):
        """The user should be shown a helpful error message."""
        response = self.client.post(
            "/",
            data={"amount": "", "from_currency": "USD", "to_currency": "GBP"},
        )
        self.assertIn(b"Please enter an amount", response.data)


if __name__ == "__main__":
    unittest.main()
