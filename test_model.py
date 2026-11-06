import unittest
from model import Inputs, calculate


class TestModel(unittest.TestCase):
    def test_initial_values(self):
        x = calculate(Inputs(cac=250, monthly_revenue=50, gross_margin_percent=70,
                             monthly_churn_percent=4))
        self.assertAlmostEqual(x.monthly_contribution, 35)
        self.assertAlmostEqual(x.ltv, 875)
        self.assertAlmostEqual(x.ltv_cac, 3.5)
        self.assertEqual(x.payback_month, 9)
        self.assertAlmostEqual(x.cumulative_after_cac[0], -250)
        self.assertAlmostEqual(x.cumulative_contribution[1], 35)
        self.assertTrue(x.net_60m < x.ltv - 250)

    def test_never_breaks_even(self):
        x = calculate(Inputs(cac=1000, monthly_revenue=10, gross_margin_percent=50,
                             monthly_churn_percent=10))
        self.assertIsNone(x.payback_month)

    def test_100_percent_churn(self):
        x = calculate(Inputs(cac=20, monthly_revenue=100, gross_margin_percent=50,
                             monthly_churn_percent=100))
        self.assertEqual(x.payback_month, 1)
        self.assertAlmostEqual(x.cumulative_contribution[60], 50)

    def test_payback_at_month_two(self):
        x = calculate(Inputs(cac=51, monthly_revenue=100, gross_margin_percent=50,
                             monthly_churn_percent=10))
        self.assertEqual(x.payback_month, 2)


if __name__ == '__main__':
    unittest.main()
