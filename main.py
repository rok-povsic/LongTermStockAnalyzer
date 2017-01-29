from dateutil.relativedelta import relativedelta

from src.finance import Finance
from src.finance_data import FinanceData
from src.plot import Plot


class Main:
    def __init__(self):
        self._finance_data = FinanceData()
        self._finance = Finance()
        self._plot = Plot()

    def run_spy(self):
        spy = self._finance_data.read_spy()
        spy_dividend_yield = self._finance_data.read_spy_dividend_yield()
        us_cpi = self._finance_data.read_us_cpi()

        years = range(1, 40 + 1)
        chance_for_years = []
        for year in years:
            print("Calculating for year:", year)
            annual_returns = self._calc_returns(
                spy, spy_dividend_yield, us_cpi, year
            )
            count_negative = len([r for r in annual_returns if r < 0])
            percent_negative = float(count_negative) / len(annual_returns) \
                * 100
            chance_for_years.append(percent_negative)
            print("Chance of losing money in a {} year period: {:.2f}%".format(
                year, percent_negative
            ))

        self._plot.plot(years, chance_for_years, "inflation adjusted")

    def _calc_returns(self, spy, spy_dividend_yield, us_cpi, years_future):
        all_dates = sorted(spy.keys())

        annual_returns = []
        for dt_current in all_dates:
            if dt_current.year == 2016 - years_future:
                break
            dt_future = dt_current + relativedelta(years=years_future)

            dts_spy = [d for d in all_dates if dt_current <= d <= dt_future]
            dts_dividends = [d + relativedelta(years=1) - relativedelta(days=1)
                             for d in dts_spy][:-1]

            spy_prices = [spy[d] for d in dts_spy]
            spy_dividends = [spy_dividend_yield[d] for d in dts_dividends]

            print("Calculating for date:", dt_current)
            print("\t", dt_current, dt_future)

            current_money = spy[dt_current]
            profit = self._finance.profit(spy_prices, spy_dividends)

            gross_ret = profit / current_money

            inflation = (us_cpi[dt_future] - us_cpi[dt_current]) / \
                us_cpi[dt_current]
            # inflation = 0
            net_ret = gross_ret - inflation

            print("{}: {:.2f}-{:.2f}={:.2f}".format(
                dt_current, gross_ret, inflation, net_ret)
            )

            annual_ret = net_ret
            annual_returns.append(annual_ret * 100)
        return annual_returns


if __name__ == '__main__':
    main = Main()
    main.run_spy()
