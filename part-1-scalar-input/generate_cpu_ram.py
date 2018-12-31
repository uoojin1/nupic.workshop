import csv
import time
import datetime
import random

with open('./data/test_data_cpu_ram.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['timestamp', 'value'])
    csv_writer.writerow(['datetime', 'int'])
    csv_writer.writerow(['T'])

    ts = time.time() # current time
    
    for i in range(10000):
        # incrementing by 10 min
        timestamp = datetime.datetime.fromtimestamp(ts + i*600).strftime('%Y-%m-%d %H:%M:%S')
        hr = datetime.datetime.fromtimestamp(ts + i*600).hour
        # print(random.gauss(50,15))
        weekday = datetime.datetime.fromtimestamp(ts + i*600).weekday()
        cpu_usage = random.gauss(50,15)
        if hr >= 16 and hr <= 20:
            cpu_usage *= random.randrange(3,4)/3
        cpu_usage /= (7-weekday)
        # print(timestamp, cpu_usage, weekday)
        csv_writer.writerow([timestamp, round(cpu_usage, 2)])
