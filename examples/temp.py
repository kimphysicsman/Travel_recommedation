import datetime
from datetime import timedelta as t

a = datetime.datetime(2021, 12, 25)

b = a + t(minutes=20)

print(a, b)