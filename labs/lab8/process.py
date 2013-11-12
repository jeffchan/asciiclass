from collections import namedtuple
import collections
import csv
from datetime import datetime

Pickup = namedtuple('Pickup', ['trip_id', 'time', 'address', 'longitude', 'latitude', 'dropoff_id'])

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dayfiles = []
daycounter = []

for day in days:
  writer = csv.writer(open(day+'.csv', 'wb'))
  writer.writerow(['latitude', 'longitude', 'count'])
  dayfiles.append(writer)
  daycounter.append(collections.Counter())

def truncate(s):
  return round(float(s), 4)

with open('pickups_train.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile)
  index = 0
  for row in reader:
    index += 1
    if index == 1:
      continue

    pickup = Pickup._make(row)
    date = datetime.strptime(pickup.time, '%Y-%m-%d %H:%M:%S').date()
    weekday = date.weekday()
    daycounter[weekday][(truncate(pickup.latitude), truncate(pickup.longitude))] += 1

for day in range(len(days)):
  counter = daycounter[day]
  csvfile = dayfiles[day]
  for pickup in counter:
    count = counter[pickup]
    csvfile.writerow([pickup[0], pickup[1], count])
