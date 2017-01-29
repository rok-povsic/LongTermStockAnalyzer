
class Finance:
    def profit(self, prices, dividends):
        """
        Calculates and returns how much profit the investor made,
        with reinvested dividends.
        """
        assert len(prices) == len(dividends) + 1
        capital_profit = prices[-1] - prices[0]
        dividend_profit = self._dividend_profit(dividends, prices)
        return capital_profit + dividend_profit

    def _dividend_profit(self, dividends, prices):
        """
        Returns the profit from dividends
        """
        dividend_profit = 0
        for i in range(len(dividends)):
            dividend = dividends[i]
            price = prices[i]
            dividend_profit += price * dividend / 100
        return dividend_profit
