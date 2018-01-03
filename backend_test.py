import USNO_scraper
import OneDayWeather
import weatherbit_caller
import pprint
import json

# Tested by hand


# -----------------------------------------------------
# Scrape data
# api_key = ""
#
# weather_data = weatherbit_caller.write_city_weather_data(api_key, city="Cambridge", state="MA", country="US",
#                             days="14", imperial_units=True, write=False)
# sun = USNO_scraper.scrape_fix_usno("sun", "2019")
# moon = USNO_scraper.scrape_fix_usno("moon", "2019")
# nautical = USNO_scraper.scrape_fix_usno("nautical twilight", "2019")
# astronomical = USNO_scraper.scrape_fix_usno("astronomical twilight", "2019")
# civil = USNO_scraper.scrape_fix_usno("civil twilight", "2019")


# -----------------------------------------------------
# Pass-in data (after running above once)
weather_data = json.loads(open("Data/weather_data_2018_1_2.json", "r+").read())  # will need to change date
sun = USNO_scraper.pass_fix_usno("Data/RAW_sun_data_2018_MA_Cambridge.html", "sun")
moon = USNO_scraper.pass_fix_usno("Data/RAW_moon_data_2018_MA_Cambridge.html", "moon")
nautical = USNO_scraper.pass_fix_usno("Data/RAW_nautical_twilight_data_2018_MA_Cambridge.html", "nautical twilight")
astronomical = USNO_scraper.pass_fix_usno("Data/RAW_astronomical_twilight_data_2018_MA_Cambridge.html", "astronomical twilight")
civil = USNO_scraper.pass_fix_usno("Data/RAW_civil_twilight_data_2018_MA_Cambridge.html", "civil twilight")

# -----------------------------------------------------
# General Case
with_weather = OneDayWeather.MultiDayWeather(weather_data, sun, moon, nautical, civil, astronomical)

# -----------------------------------------------------
# Change to Daylight Savings Time and Date Input
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "6", "2018", "3", "18")

# -----------------------------------------------------
# Rollover on Daylight Savings Time on 23** time
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "20", "2018", "3", "27")

# -----------------------------------------------------
# Multiple Years
sun = [sun, USNO_scraper.pass_fix_usno("Data/RAW_sun_data_2019_MA_Cambridge.html", "sun", "2019")]
moon = [moon, USNO_scraper.pass_fix_usno("Data/RAW_moon_data_2019_MA_Cambridge.html", "moon", "2019")]
nautical = [nautical, USNO_scraper.pass_fix_usno("Data/RAW_nautical_twilight_data_2019_MA_Cambridge.html", "nautical twilight", "2019")]
astronomical = [astronomical, USNO_scraper.pass_fix_usno("Data/RAW_astronomical_twilight_data_2019_MA_Cambridge.html", "astronomical twilight", "2019")]
civil = [civil, USNO_scraper.pass_fix_usno("Data/RAW_civil_twilight_data_2019_MA_Cambridge.html", "civil twilight", "2019")]
with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "12", "28", "2019", "1", "2")

# -----------------------------------------------------
# Printer
for one_day in with_weather.one_days:
    pprint.pprint(one_day)