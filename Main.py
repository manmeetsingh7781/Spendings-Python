import re
import operator
import matplotlib.pyplot as plt


def get_totals(each_list):
    total = 0
    for each in each_list:
        total += float(each)
    return round(total, 2)



def calculate_total(file_name):
    total_amount = 0
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
    results_by_name = sorted({get_totals(food): 'Restaurants/Dining',
                      get_totals(gas): 'Gasoline/Fuel', get_totals(other): 'Other Expenses',
                      get_totals(entertainment): 'Entertainment',
                      get_totals(electronics): 'Electronics'}.items(), key=operator.itemgetter(0))

    payments_returns_results =  {get_totals(payments_returns): payments_returns,
                                 get_totals(payments_returns): 'Payments and Returns'}

    print("Total $" + str(round(total_amount, 2)))

    chart_setup = []

    labels = []
    sizes = []
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

    plt.pie(sizes,  labels=labels,
            autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    calculate_total('C:\\Users\\manme\\Desktop\\ExportData.csv')
