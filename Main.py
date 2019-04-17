# Manmeet Singh


import re


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
        if 'Restaurants/Dining' in each:
            food.append(matcher.group().replace('$,-', ''))

        if 'Other Expenses' in each:
            other.append(matcher.group().replace('$,-', ''))

        if 'Gasoline/Fuel' in each:
            gas.append(matcher.group().replace('$,-', ''))

        if 'Entertainment' in each:
            entertainment.append(matcher.group().replace('$,-', ''))

        if 'General Merchandise' in each:
            other.append(matcher.group().replace('$,-', ''))

        if 'Automotive Expenses' in each:
            other.append(matcher.group().replace('$,-', ''))

        if 'Electronics' in each:
            electronics.append(matcher.group().replace('$,-', ''))

        if 'Other Income' in each:
            payments_returns.append(matcher.group().replace('$,', ''))

        if 'Service Charges/Fees' in each:
            other.append(matcher.group().replace('$,-', ''))

        if 'Card Payments' in each:
            payments_returns.append(matcher.group().replace('$,', ''))

        if matcher:
            each_group = matcher.group()
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


if __name__ == '__main__':
    calculate_total('Data.csv')

