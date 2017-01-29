import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Plot:
    def plot(self, years, chance_for_years, subtitle):
        self._setup_plot()
        ax = plt.gca()
        ax.set_title('Chance of losing money being invested in S&P 500 '
                     'for a number of years,\n' +
                     subtitle)
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

    def _setup_plot(self):
        sns.set_palette(sns.color_palette())
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: "{:,}%".format(int(x)))
        )
