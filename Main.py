import re
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

    print(dates[-1] + " through " + dates[0])
    print("food: $" + str(get_totals(food)))
    print("payments_returns: $" + str(get_totals(payments_returns)))
    print("gas: $" + str(get_totals(gas)))
    print("other: $" + str(get_totals(other)))
    print("entertainment: $" + str(get_totals(entertainment)))
    print("electronics: $" + str(get_totals(electronics)))
    print("Total $" + str(round(float(total_amount))))
    print(len(food))
    print(len(payments_returns))
    print(len(gas))
    print(len(other))
    print(len(entertainment))
    print(len(electronics))
    print(len(dates))
    #x = np.linspace(0, 2, 100)
    #plt.plot(food, dates, label='Food')
    # # plt.plot(x, x**2, label='quadratic')
    # # plt.plot(x, x**3, label='cubic')
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title("Simple Plot")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    calculate_total('Data.csv')
