import weatherbit_caller
import USNO_scraper
import OneDayWeather
import json
import pprint

# api_key = ""
#
# weather_data = weatherbit_caller.write_city_weather_data(api_key, city="Cambridge", state="MA", country="US",
#                             days="14", imperial_units=True, write=False)
# sun = USNO_scraper.scrape_fix_usno("sun")
# moon = USNO_scraper.scrape_fix_usno("moon")
# nautical = USNO_scraper.scrape_fix_usno("nautical twilight")
# astronomical = USNO_scraper.scrape_fix_usno("astronomical twilight")
# civil = USNO_scraper.scrape_fix_usno("civil twilight")



# weather_data = json.loads(open("Data/weather_data_2018_1_2.json", "r+").read())
sun = USNO_scraper.pass_fix_usno("Data/RAW_sun_data_2018_MA_Cambridge.html", "sun")
moon = USNO_scraper.pass_fix_usno("Data/RAW_moon_data_2018_MA_Cambridge.html", "moon")
nautical = USNO_scraper.pass_fix_usno("Data/RAW_nautical_twilight_data_2018_MA_Cambridge.html", "nautical twilight")
astronomical = USNO_scraper.pass_fix_usno("Data/RAW_astronomical_twilight_data_2018_MA_Cambridge.html", "astronomical twilight")
civil = USNO_scraper.pass_fix_usno("Data/RAW_civil_twilight_data_2018_MA_Cambridge.html", "civil twilight")

# with_weather = OneDayWeather.MultiDayWeather(weather_data, sun, moon, nautical, civil, astronomical)

# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "6", "2018", "3", "18")
with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "20", "2018", "3", "27")
for one_day in with_weather.one_days:
    pprint.pprint(one_day)