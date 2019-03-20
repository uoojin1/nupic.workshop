import time
import datetime
import random

def generateRandomUsageData():  
    ts = time.time() # current time
    #i = 0
    #while i < 1000:
    while true:
      timestamp = datetime.datetime.fromtimestamp(ts + i*3600).strftime('%Y-%m-%d %H:%M:%S')
      hr = datetime.datetime.fromtimestamp(ts + i*3600).hour
      weekday = datetime.datetime.fromtimestamp(ts + i*3600).weekday()
      cpu_usage = random.gauss(50,10)
      if hr >= 16 and hr <= 20:
          cpu_usage *= random.randrange(3,4)/3
      cpu_usage /= (7-weekday)
      yield (timestamp, cpu_usage)
      #i+=1