import csv
import os

from datetime import datetime
from decimal import Decimal


class FinanceData:
    _data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    def read_spy(self):
        dt_to_price = {}
        with open(os.path.join(self._data_dir, "sp500.csv")) as f:
            for row in csv.reader(f):
                dt = datetime.strptime(row[0], "%b %d %Y")
                price = Decimal(row[1])
                dt_to_price[dt] = price
        return dt_to_price

    def read_spy_dividend_yield(self):
        dt_to_yield = {}
        with open(os.path.join(self._data_dir, "sp500_dividend_yield.csv")) \
                as f:
            for row in csv.reader(f):
                dt = datetime.strptime(row[0], "%b %d %Y")
                price = Decimal(row[1].replace("%", ""))
                dt_to_yield[dt] = price
        return dt_to_yield

    def read_us_cpi(self):
        dt_to_cpi = {}
        with open(os.path.join(self._data_dir, "us_cpi.csv")) as f:
            for row in csv.reader(f):
                dt = datetime.strptime(row[0], "%b %d %Y")
                price = Decimal(row[1].replace("%", ""))
                dt_to_cpi[dt] = price
        return dt_to_cpi
