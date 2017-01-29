
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import pandas as pd
import seaborn as sns

from matplotlib.ticker import FuncFormatter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from src.finance import Finance


class Main:
    def __init__(self):
        self._finance = Finance()

    def run_basic(self):
        dt_to_price = self._read_djia()
        dts = sorted(dt_to_price.keys())
        prices = [dt_to_price[dt] for dt in dts]

        self._setup_plot()
        plt.yscale('log')

        ax = plt.gca()
        ax.get_yaxis().set_major_formatter(
            FuncFormatter(lambda y, p: "$" + format(int(y), ',')))

        plt.plot(dts, prices)
        plt.show()

    def run_returns(self, years_future):
        dt_to_price = self._read_djia()
        dts = sorted(dt_to_price.keys())

        annual_returns = self._calc_returns(dt_to_price, dts, years_future)

        returns_dts = dts[:len(annual_returns)]

        count_negative = len([r for r in annual_returns if r < 0])
        percent_negative = float(count_negative) / len(annual_returns) * 100
        print("Chance of losing money in a {} year period: {:.2f}%".format(
            years_future, percent_negative
        ))

        self._setup_plot()
        plt.plot(returns_dts, annual_returns)
        plt.show()

    def run_spy(self):
        spy = self._read_spy()
        spy_dividend_yield = self._read_spy_dividend_yield()
        us_cpi = self._read_us_cpi()

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

        self._setup_plot()

        ax = plt.gca()
        ax.set_title('Chance of losing money being invested in S&P 500 '
                     'for a number of years,\n'
                     'inflation adjusted')
        ax.set_ylabel('Percentage chance of losing money')
        ax.set_xlabel('Years of being invested')

        ax.title.set_fontsize(15)
        ax.xaxis.label.set_fontsize(14)
        ax.yaxis.label.set_fontsize(14)

        print(years)
        print(chance_for_years)

        plt.bar(years, chance_for_years)
        plt.xlim([min(years), max(years) + 1])
        plt.show()

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

    def _setup_plot(self):
        sns.set_palette(sns.color_palette())
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: "{:,}%".format(int(x)))
        )

    def _read_spy(self):
        dt_to_price = {}
        with open("sp500.csv") as f:
            for row in csv.reader(f):
                dt = datetime.strptime(row[0], "%b %d %Y")
                price = Decimal(row[1])
                dt_to_price[dt] = price
        return dt_to_price

    def _read_spy_dividend_yield(self):
        dt_to_yield = {}
        with open("sp500_dividend_yield.csv") as f:
            for row in csv.reader(f):
                dt = datetime.strptime(row[0], "%b %d %Y")
                price = Decimal(row[1].replace("%", ""))
                dt_to_yield[dt] = price
        return dt_to_yield

    def _read_us_cpi(self):
        dt_to_cpi = {}
        with open("us_cpi.csv") as f:
            for row in csv.reader(f):
                dt = datetime.strptime(row[0], "%b %d %Y")
                price = Decimal(row[1].replace("%", ""))
                dt_to_cpi[dt] = price
        return dt_to_cpi

    def _read_djia(self):
        csv_file = pd.read_csv("djia.csv")
        csv_file.set_index(["Date"], inplace=True)
        csv_file = csv_file.sort_index()
        dts = [datetime.strptime(dt_str, "%Y-%m-%d")
               for dt_str in csv_file.index.values]
        dts = [dt for dt in dts if dt <= datetime(2018, 1, 1)]
        values = csv_file["Value"][:len(dts)]

        dt_to_price = dict(zip(dts, values))
        return dt_to_price

    def _read_gold(self):
        csv_file = pd.read_csv("gold.csv")
        csv_file.set_index(["Date"], inplace=True)
        csv_file = csv_file.sort_index()
        dts = [datetime.strptime(dt_str, "%Y-%m-%d")
               for dt_str in csv_file.index.values]
        dts = [dt for dt in dts if dt <= datetime(2018, 1, 1)]
        values = csv_file["USD (PM)"][:len(dts)]

        dt_to_price = dict(zip(dts, values))
        return dt_to_price


if __name__ == '__main__':
    # Main().run_basic()
    # Main().run_returns(3)
    main = Main()
    main.run_spy()
