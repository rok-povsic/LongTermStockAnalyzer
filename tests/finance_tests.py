import unittest

from src.finance import Finance


class FinanceTests(unittest.TestCase):
    def test_profit_for_one_year(self):
        finance = Finance()

        prices = [100, 101]
        dividends = [2]

        capital_profit = 1  # 101 - 100
        dividend_profit = 100 * 0.02
        total_profit = capital_profit + dividend_profit

        self.assertAlmostEqual(total_profit, finance.profit(prices, dividends))

    def test_profit_for_two_years(self):
        finance = Finance()

        prices = [100, 99, 101]
        dividends = [2, 3]

        capital_profit = 1  # 101 - 100
        dividend_profit = 100 * 0.02 + 99 * 0.03
        total_profit = capital_profit + dividend_profit

        self.assertAlmostEqual(total_profit, finance.profit(prices, dividends))

    def test_profit_for_three_years(self):
        finance = Finance()

        prices = [100, 99, 101, 80]
        dividends = [2, 3, 1]

        capital_profit = -20  # 101 - 100
        dividend_profit = 100 * 0.02 + 99 * 0.03 + 101 * 0.01
        total_profit = capital_profit + dividend_profit

        self.assertAlmostEqual(total_profit, finance.profit(prices, dividends))
