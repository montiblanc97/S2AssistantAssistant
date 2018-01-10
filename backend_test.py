import twilight_scraper
import OneDayWeather
import weatherbit_caller
import pprint
import json
import commander

# Tested by hand


# -----------------------------------------------------
# Scrape data
# api_key = ""
#
# weather_data = weatherbit_caller.write_city_weather_data(api_key, city="Cambridge", state="MA", country="US",
#                             days="14", imperial_units=True, write=False)
# sun = twilight_scraper.twilight_scrape_fix("sun", "2019", "Cambridge", "MA", "eastern", True, True, True)
# moon = twilight_scraper.twilight_scrape_fix("moon", "2019", "Cambridge", "MA", "eastern", True, True, True)
# nautical = twilight_scraper.twilight_scrape_fix("nautical twilight", "2019", "Cambridge", "MA", "eastern", True, True,
#                                                 True)
# astronomical = twilight_scraper.twilight_scrape_fix("astronomical twilight", "2019", "Cambridge", "MA", "eastern", True,
#                                                     True, True)
# civil = twilight_scraper.twilight_scrape_fix("civil twilight", "2019", "Cambridge", "MA", "eastern", True, True, True)


# -----------------------------------------------------
# Pass-in data (after running above once)
# weather_data = json.loads(open("Data/weather_data_2018_1_2.json", "r+").read())  # will need to change date
# sun = twilight_scraper.twilight_pass_fix("Data/RAW_sun_data_2018_MA_Cambridge.html", "sun", "2018", "Cambridge",
#                                          "MA", "eastern", False, False)
# moon = twilight_scraper.twilight_pass_fix("Data/RAW_moon_data_2018_MA_Cambridge.html", "moon", "2018", "Cambridge",
#                                           "MA", "eastern", False, False)
# nautical = twilight_scraper.twilight_pass_fix("Data/RAW_nautical_twilight_data_2018_MA_Cambridge.html",
#                                               "nautical twilight", "2018", "Cambridge", "MA", "eastern", False, False)
# astronomical = twilight_scraper.twilight_pass_fix("Data/RAW_astronomical_twilight_data_2018_MA_Cambridge.html",
#                                                   "astronomical twilight", "2018", "Cambridge", "MA", "eastern", False,
#                                                   False)
# civil = twilight_scraper.twilight_pass_fix("Data/RAW_civil_twilight_data_2018_MA_Cambridge.html", "civil twilight",
#                                            "2018", "Cambridge", "MA", "eastern", False, False)

# -----------------------------------------------------
# General Case
# with_weather = OneDayWeather.MultiDayWeather(weather_data, sun, moon, nautical, civil, astronomical)

# -----------------------------------------------------
# Change to Daylight Savings Time and Date Input
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "6", "2018", "3", "18")

# -----------------------------------------------------
# Rollover on Daylight Savings Time on 23** time
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "20", "2018", "3", "27")

# -----------------------------------------------------
# Multiple Years
# sun = [sun,
#        twilight_scraper.twilight_pass_fix("Data/RAW_sun_data_2019_MA_Cambridge.html", "sun", "2019", "Cambridge", "MA",
#                                           "eastern", False, False)]
# moon = [moon,
#         twilight_scraper.twilight_pass_fix("Data/RAW_moon_data_2019_MA_Cambridge.html", "moon", "2019", "Cambridge",
#                                            "MA", "eastern", False, False)]
# nautical = [nautical, twilight_scraper.twilight_pass_fix("Data/RAW_nautical_twilight_data_2019_MA_Cambridge.html",
#                                                          "nautical twilight", "2019", "Cambridge", "MA", "eastern",
#                                                          False, False)]
# astronomical = [astronomical,
#                 twilight_scraper.twilight_pass_fix("Data/RAW_astronomical_twilight_data_2019_MA_Cambridge.html",
#                                                    "astronomical twilight", "2019", "Cambridge", "MA", "eastern", False,
#                                                    False)]
# civil = [civil,
#          twilight_scraper.twilight_pass_fix("Data/RAW_civil_twilight_data_2019_MA_Cambridge.html", "civil twilight",
#                                             "2019", "Cambridge", "MA", "eastern", False, False)]
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "12", "28", "2019",
#                                              "1", "2")

# -----------------------------------------------------
# create_rep pass in
# with_weather = commander.create_rep(weather_data, sun, moon, nautical, astronomical, civil)

# -----------------------------------------------------
# create_rep scrape
parameters = {"api_key": "", "city": "Cambridge", "state": "MA", "days": "14", "write_weather": True,
              "write_unfixed_dict": True, "write_fixed_dict": True, "imperial_units": True, "write_html": True}
with_weather = commander.create_rep(True, True, True, True, True, True, parameters)

# -----------------------------------------------------
# create_rep scrape multi year CAREFUL might scrape too much
# parameters = {"city": "Cambridge", "state": "MA", "days": "14", "write_weather": True, "write_unfixed_dict": True,
#               "write_fixed_dict": True, "imperial_units": True, "write_html": True, "year_start": "2018",
#               "month_start":"12", "day_start": "30", "year_end": "2020", "month_end": "1", "day_end": "1",
#               "timezone": "eastern"}
# with_weather = commander.create_rep(False, True, True, True, True, True, parameters)

# -----------------------------------------------------
# Printer
for one_day in with_weather.one_days:
    pprint.pprint(one_day)
