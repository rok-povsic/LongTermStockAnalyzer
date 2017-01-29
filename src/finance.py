
class Finance:
    def profit(self, prices, dividends):
        """
        Calculates and returns how much profit the investor made,
        with reinvested dividends.
        """
        assert len(prices) == len(dividends) + 1
        capital_profit = prices[-1] - prices[0]
        dividend_profit = 0
        for i in range(len(dividends)):
            dividend = dividends[i]
            price = prices[i]
            dividend_profit += price * dividend / 100
        return capital_profit + dividend_profit
