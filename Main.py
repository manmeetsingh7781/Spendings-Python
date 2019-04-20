import re
import operator
import numpy as np
import matplotlib.pyplot as plt


def get_totals(each_list):
    total = 0
    for each in each_list:
        total += float(each)
    return round(total, 2)


def calculate_total(file_name):
    total_amount = 0
    counter = 0
    records, chart_setup, labels, sizes, dates, food, payments_returns, gas, other,  entertainment, electronics = ([], [],[],[] ,[], [], [], [], [], [], [])
    file = open(file_name, 'r')
    file_data = list(file.readlines())
    for each in file_data:
        date = re.search(r',\d+/\d+/\d+', each)
        if date:
            dates.append(date.group().replace(',', ''))
        pattern = r'\$.+.[.+, .+]\d+'
        matcher = re.search(pattern, each)
        if matcher:
            each_group = matcher.group()

            if 'Restaurants/Dining' in each:
                food.append(each_group.replace('$,-', ''))
            else:
                food.append('0')

            if 'Other Expenses' in each:
                other.append(matcher.group().replace('$,-', ''))
            elif 'Service Charges/Fees' in each:
                other.append(matcher.group().replace('$,-', ''))
            elif 'Automotive Expenses' in each:
                other.append(matcher.group().replace('$,-', ''))
            elif 'General Merchandise' in each:
                other.append(matcher.group().replace('$,-', ''))
            else:
                other.append('0')

            if 'Card Payments' in each:
                payments_returns.append(matcher.group().replace('$,', ''))
            elif 'Other Income' in each:
                payments_returns.append(matcher.group().replace('$,', ''))
            else:
                payments_returns.append('0')

            if 'Gasoline/Fuel' in each:
                gas.append(matcher.group().replace('$,-', ''))
            else:
                gas.append('0')

            if 'Entertainment' in each:
                entertainment.append(matcher.group().replace('$,-', ''))
            else:
                entertainment.append('0')

            if 'Electronics' in each:
                electronics.append(matcher.group().replace('$,-', ''))
            else:
                electronics.append('0')

            if not each_group.find("$,-"):
                digit_finder = re.search(r'\d(\d)*.(\d)*', each_group)
                if digit_finder:
                    total_amount += float(digit_finder.group().replace(',', ''))
    results_by_name = sorted({get_totals(food): 'Restaurants/Dining',
                      get_totals(gas): 'Gasoline/Fuel', get_totals(other): 'Other Expenses',
                      get_totals(entertainment): 'Entertainment',
                      get_totals(electronics): 'Electronics'}.items(), key=operator.itemgetter(0))
    calculate_percentage = lambda n: round((n/total_amount)*100, 2)
    for each_item in results_by_name:
        data = dict()
        data[calculate_percentage(each_item[0])] = each_item[1]
        chart_setup.append(data)
    for items in chart_setup:
        for i in items.values():
            labels.append(i)
        for x in items.keys():
            sizes.append(x)
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    for i in results_by_name:
        f = "$" + str(i[0]) + " " + i[1] + ", " + str(sizes[counter]) + "%"
        counter += 1
        records.append(f)
    wedges, texts = ax.pie(sizes, wedgeprops=dict(width=0.5), startangle=-65)
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
        ax.annotate(records[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, **kw)
    ax.set_title("\n\nWarning: All of these calculations are rounded to the nearest k, and Payments & returns are not included in total\nData Records through " + dates[-1] + " to " + dates[0] + " \n" + " Total-Spending: $" + str(round(total_amount, 2))+ "\nPayments & Returns: $" + str(get_totals(payments_returns)))
    plt.show()
    
    
if __name__ == '__main__':
    calculate_total('C:\\Users\\manme\\Desktop\\ExportData.csv')
