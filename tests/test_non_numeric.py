"""Task 2(b): If the user enters a non-numeric input, the app should not
crash - it should return a normal page with an error message."""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app


class TestNonNumericInput(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_non_numeric_amount_does_not_crash(self):
        """Submitting text instead of a number should return HTTP 200, not a 500 crash."""
        response = self.client.post(
            "/",
            data={"amount": "abc", "from_currency": "GBP", "to_currency": "EUR"},
        )
        self.assertEqual(response.status_code, 200)

    def test_non_numeric_amount_shows_error_message(self):
        """The user should be shown a helpful error message."""
        response = self.client.post(
            "/",
            data={"amount": "ten pounds", "from_currency": "GBP", "to_currency": "EUR"},
        )
        self.assertIn(b"Please enter a valid number", response.data)


if __name__ == "__main__":
    unittest.main()
