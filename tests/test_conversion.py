"""Task 2(c): Verify conversions are performed correctly for:
    10 USD -> GBP, 1 GBP -> EUR, 23 EUR -> USD
Rates are hard-coded in app.py: USD->GBP 0.79, GBP->EUR 1.16, EUR->USD 1.09."""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app


class TestConversion(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def _convert(self, amount, from_currency, to_currency):
        return self.client.post(
            "/",
            data={
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            },
        )

    def test_10_usd_to_gbp(self):
        """10 USD x 0.79 = 7.9 GBP"""
        response = self._convert("10", "USD", "GBP")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"7.9", response.data)

    def test_1_gbp_to_eur(self):
        """1 GBP x 1.16 = 1.16 EUR"""
        response = self._convert("1", "GBP", "EUR")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"1.16", response.data)

    def test_23_eur_to_usd(self):
        """23 EUR x 1.09 = 25.07 USD"""
        response = self._convert("23", "EUR", "USD")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"25.07", response.data)


if __name__ == "__main__":
    unittest.main()
