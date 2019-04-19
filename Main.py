import re
import operator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def get_totals(each_list):
    total = 0
    for each in each_list:
        total += float(each)
    return round(total)


def calculate_total(file_name):
    total_amount = 0

    # payments_returns  are not spendings
    dates, food, payments_returns, gas, other,  entertainment, electronics = ([], [], [], [], [], [], [])
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

    print("Warning: All of these calculations are rounded to the nearest k, and Payments & returns are not included in total")
    print(dates[-1] + " through " + dates[0])
    # print(get_totals(food, "food"))
    # print(get_totals(payments_returns, "payments and returns"))
    # print(get_totals(gas, "gas"))
    # print(get_totals(other, 'other'))
    # print(get_totals(entertainment, 'entertainment'))
    # print(get_totals(electronics, 'electronics'))

    results = sorted({get_totals(food): 'Food', get_totals(payments_returns):'Payments and Returns',
               get_totals(gas): 'Gas', get_totals(other): 'Other',
               get_totals(entertainment): 'Entertainment',
               get_totals(electronics): 'Electronics'}.items(), key=operator.itemgetter(0))

    print(results)

    print("Total $" + str(round(float(total_amount))))
    # plt.title("Bank Account")
    # plt.plot(dates, food, label='Food')
    # plt.plot(dates, gas, label='Gas')
    # plt.plot(dates, payments_returns, label='Payments and Returns')
    # plt.plot(dates, entertainment, label='Entertainment')
    # plt.plot(dates, electronics, label='Electronics')
    # plt.plot(dates, other, label='Other')
    # plt.xlabel('Dates')
    # plt.ylabel('Spending')
    # plt.title("Bank Status")
    # plt.legend()
    # plt.show()


if __name__ == '__main__':
    calculate_total('Data.csv')
