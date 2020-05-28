import json

def refix_json(field):
    path = 'C:\\Users\\Pende\\Documents\\myapps\\my_machine_learning\\data\\raw.json'
    new_file = 'C:\\Users\\Pende\\Documents\\myapps\\my_machine_learning\\data\\new_raw.json'
    new_data = []
    with open(path, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            try:
                data_to_append = item[field]
            except KeyError:
                break
            else:
                new_data.append(data_to_append)
        with open(new_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=4)

# refix_json('fields')

import datetime
import calendar

start = datetime.datetime.now().now()
end = datetime.datetime.strptime('2019-01-04', '%Y-%m-%d')
value = (start - end).days
value = start > end

current_date = datetime.datetime.now().date()
last_day_of_month = calendar.monthrange(2019, current_date.month)
# print(last_day_of_month)

def test():
    for m in range(1, 12):
        d = calendar.monthrange(2020, m)
        month_range = [f'2020-{m}-1', f'2020-{m}-{d[1]}']
        e = [datetime.datetime.strptime(m, '%Y-%m-%d') for m in month_range]
        yield e

# print(list(test()))
print(list(test())[0][0].day > current_date.day)
# print(datetime.datetime(2019, 2, 5).timestamp())