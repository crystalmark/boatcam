import datetime
from suntime import Sun, SunTimeException

latitude = 55.982282667
longitude = -3.219525287

sun = Sun(round(latitude,2), round(longitude,2))

# Get today's sunrise and sunset in UTC
today_sr = sun.get_sunrise_time()
today_ss = sun.get_sunset_time()

timezone = today_sr.tzinfo

print('Today at the boat the sun raised at {} and go down at {} local time'.
      format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

if today_sr < datetime.datetime.now(timezone) < today_ss:
	print("Daylight")
else:
	print("Nighttime")