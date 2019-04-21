import re
import operator
import numpy as np
import matplotlib.pyplot as plt


class BoFA:
    c = 0
    def __init__(self, path):
        self.path = path
        self._total_amount = 0
        self._counter = 0

        self._calculating = False
        self._records, self._chart_setup, self._labels, self._sizes, self._dates, self._food, self._payments_returns,\
        self._gas, self._other, self._entertainment, self._electronics, self._money, self._final_recs = ([], [], [], [], [], [], [], [], [], [], [], [], [])

    @staticmethod
    def get_totals(each_list):
        total = 0
        for each in each_list:
            total += float(each)
        return round(total, 2)

    # Takes a file and calculates the Spendings
    def calculate_total(self, drawing):
        self._calculating = True
        file = open(self.path, 'r')
        file_data = list(file.readlines())
        for each in file_data:
            date = re.search(r',\d+/\d+/\d+', each)
            if date:
                self._dates.append(date.group().replace(',', ''))
            pattern = r'\$.+.[.+, .+],+'
            matcher = re.search(pattern, each)
            if matcher:
                self.c +=1
                each_group = matcher.group().replace(',,,', '').replace('$,', '')
                if 'Restaurants/Dining' in each:
                    self._food.append(each_group.replace('-', ''))
                else:
                    self._food.append(0)

                if 'Other Expenses' in each:
                    self._other.append(abs(float(each_group)))
                elif 'Service Charges/Fees' in each:
                    self._other.append(abs(float(each_group)))
                elif 'Automotive Expenses' in each:
                    self._other.append(abs(float(each_group)))
                elif 'General Merchandise' in each:
                    self._other.append(abs(float(each_group)))
                else:
                    self._other.append(0)

                if 'Card Payments' in each:
                    self._payments_returns.append(abs(float(each_group)))
                elif 'Other Income' in each:
                    self._payments_returns.append(abs(float(each_group)))
                else:
                    self._payments_returns.append(0)

                if 'Gasoline/Fuel' in each:
                    self._gas.append(abs(float(each_group)))
                else:
                    self._gas.append(0)

                if 'Entertainment' in each:
                    self._entertainment.append(abs(float(each_group)))
                else:
                    self._entertainment.append(0)

                if 'Electronics' in each:
                    self._electronics.append(abs(float(each_group)))
                else:
                    self._electronics.append(0)


        self._total_amount = self.get_totals(self._food) + self.get_totals(self._gas) + self.get_totals(self._entertainment) + self.get_totals(self._electronics) + self.get_totals(self._other)

        results_by_name = sorted({self.get_totals(self._food): 'Restaurants/Dining',
                                  self.get_totals(self._gas): 'Gasoline/Fuel', self.get_totals(self._other): 'Other Expenses',
                                  self.get_totals(self._entertainment): 'Entertainment',
                                  self.get_totals(self._electronics): 'Electronics'}.items(), key=operator.itemgetter(0))
        calculate_percentage = lambda n: round((n / self._total_amount) * 100, 2)

        for each_item in results_by_name:
            data = dict()
            self._money.append(each_item[0])
            data[calculate_percentage(each_item[0])] = each_item[1]
            self._chart_setup.append(data)

        for items in self._chart_setup:
            for i in items.values():
                self._labels.append(i)
            for x in items.keys():
                self._sizes.append(x)

        for i in results_by_name:
            f = "$" + str(i[0]) + " - " + i[1] + ", " + str(self._sizes[self._counter]) + "%"
            ff = "$" + str(i[0]) + " - " + i[1]

            self._counter += 1
            self._records.append(f)
            self._final_recs.append(ff)
        self._total_amount = round(self._total_amount, 2)
        if drawing:
            self.draw()

    # Draws a graph to the screen
    def draw(self, calculations=True):

        if not calculations:
            calculations = True
        if calculations and not self._calculating:
            self.calculate_total(False)

        fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(aspect="equal"))
        wedges, texts = ax.pie(self._sizes, wedgeprops=dict(width=0.5), startangle=-65)
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(self._records[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment, **kw)
        ax.set_title(
            "\n\nWarning: All of these calculations are rounded to the nearest k, and Payments & returns are not included in total\nData Records through " +
            self._dates[-1] + " to " + self._dates[0] + " \n" + " Total-Spending: $" + str(
                round(self._total_amount, 2)) + "\nPayments & Returns: $" + str(
                self.get_totals(self._payments_returns)))

        plt.show()

    # Add two Bank Accounts and compare it
    def __add__(self, other):

        self.calculate_total(False)
        other.calculate_total(False)
        fig, axes = plt.subplots(1, 2, figsize=(12, 8))
        chart = []
        for i, ax in enumerate(axes.flatten()):
            chart.append(ax)

        chart[0].set_title(self._dates[-1] + " through " + self._dates[0] + "\nPayments & Returns: $" + str(
                self.get_totals(self._payments_returns)) + "\nTotal-Spending: $" + str(self._total_amount))
        chart[1].set_title(other._dates[-1] + " through " + other._dates[0] + "\nPayments & Returns: $" + str(
            other.get_totals(other._payments_returns)) + "\nTotal-Spending: $" + str(other._total_amount))
        chart[0] = chart[0].pie(self._sizes, labels=(self._final_recs), radius=1, autopct="%.1f%%", pctdistance=0.9)
        chart[1] = chart[1].pie(other._sizes, labels=(other._final_recs), radius=1, autopct="%.1f%%", pctdistance=0.9)
        plt.legend(self._labels, bbox_to_anchor=(1, 0), loc="upper right",)
        plt.show()


if __name__ == '__main__':
    one_month = BoFA(path='C:\\Users\Honey Singh\\Desktop\\ExportData.csv')
    last_three_months = BoFA(path='C:\\Users\Honey Singh\\Desktop\\ExportData3months.csv')
    # Adding two Objects and Comparing it
    one_month + last_three_months
    
    # Calling single object
    one_month.draw()
