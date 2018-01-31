import json

import backend.twilight_scraper as twilight_scraper
import backend.weather_reps as weather_reps
import backend.complete_rep as complete_rep

# Tested by hand


# -----------------------------------------------------
# Scrape data
# api_key = ""
#
# weather_data = weatherbit_caller.write_city_weather_data(api_key, city="Cambridge", state="MA", country="US",
#                             days="14", imperial_units=True, write=False)
# sun = twilight_scraper.twilight_scrape("sun", "2019", "Cambridge", "MA", "eastern", True, True, True)
# moon = twilight_scraper.twilight_scrape("moon", "2019", "Cambridge", "MA", "eastern", True, True, True)
# nautical = twilight_scraper.twilight_scrape("nautical twilight", "2019", "Cambridge", "MA", "eastern", True, True,
#                                                 True)
# astronomical = twilight_scraper.twilight_scrape("astronomical twilight", "2019", "Cambridge", "MA", "eastern", True,
#                                                     True, True)
# civil = twilight_scraper.twilight_scrape("civil twilight", "2019", "Cambridge", "MA", "eastern", True, True, True)


# -----------------------------------------------------
# Pass-in data (after running above once)
weather_data = json.loads(open("Data/weather_data_2018_1_2.json", "r+").read())  # will need to change date after scrape
sun = twilight_scraper.twilight_pass("Data/RAW_sun_data_2018_MA_Cambridge.html", "sun", "2018", "Cambridge",
                                     "MA", "eastern")
moon = twilight_scraper.twilight_pass("Data/RAW_moon_data_2018_MA_Cambridge.html", "moon", "2018", "Cambridge",
                                      "MA", "eastern")
nautical = twilight_scraper.twilight_pass("Data/RAW_nautical_twilight_data_2018_MA_Cambridge.html",
                                          "nautical twilight", "2018", "Cambridge", "MA", "eastern")
astronomical = twilight_scraper.twilight_pass("Data/RAW_astronomical_twilight_data_2018_MA_Cambridge.html",
                                              "astronomical twilight", "2018", "Cambridge", "MA", "eastern")
civil = twilight_scraper.twilight_pass("Data/RAW_civil_twilight_data_2018_MA_Cambridge.html", "civil twilight",
                                       "2018", "Cambridge", "MA", "eastern")

# -----------------------------------------------------
# General Case
with_weather = weather_reps.MultiDayData(weather_data, sun, moon, nautical, civil, astronomical)

# -----------------------------------------------------
# Change to Daylight Savings Time and Date Input
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "6", "2018", "3", "18")

# -----------------------------------------------------
# Rollover on Daylight Savings Time on 23** time
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "3", "20", "2018", "3", "27")

# -----------------------------------------------------
# Multiple Years
# sun = [sun,
#        twilight_scraper.twilight_pass("Data/RAW_sun_data_2019_MA_Cambridge.html", "sun", "2019", "Cambridge", "MA",
#                                           "eastern")]
# moon = [moon,
#         twilight_scraper.twilight_pass("Data/RAW_moon_data_2019_MA_Cambridge.html", "moon", "2019", "Cambridge",
#                                            "MA", "eastern")]
# nautical = [nautical, twilight_scraper.twilight_pass("Data/RAW_nautical_twilight_data_2019_MA_Cambridge.html",
#                                                          "nautical twilight", "2019", "Cambridge", "MA", "eastern",
#                                                          False, False)]
# astronomical = [astronomical,
#                 twilight_scraper.twilight_pass("Data/RAW_astronomical_twilight_data_2019_MA_Cambridge.html",
#                                                    "astronomical twilight", "2019", "Cambridge", "MA", "eastern", False,
#                                                    False)]
# civil = [civil,
#          twilight_scraper.twilight_pass("Data/RAW_civil_twilight_data_2019_MA_Cambridge.html", "civil twilight",
#                                             "2019", "Cambridge", "MA", "eastern")]
# with_weather = OneDayWeather.MultiDayWeather(None, sun, moon, nautical, civil, astronomical, "2018", "12", "28", "2019",
#                                              "1", "2")

# -----------------------------------------------------
# create_rep pass in
with_weather = complete_rep.create_rep(weather_data, sun, moon, nautical, astronomical, civil)

# -----------------------------------------------------
# create_rep scrape
# parameters = {"api_key": "", "city": "Cambridge", "state": "MA", "days": "14", "write_weather": True,
#               "write_unfixed_dict": True, "write_fixed_dict": True, "imperial_units": True, "write_html": True}
# with_weather = commander.create_rep(True, True, True, True, True, True, parameters)

# -----------------------------------------------------
# create_rep scrape multi year ***CAREFUL might scrape too much***
# parameters = {"city": "Cambridge", "state": "MA", "days": "14", "write_weather": True, "write_unfixed_dict": True,
#               "write_fixed_dict": True, "imperial_units": True, "write_html": True, "year_start": "2018",
#               "month_start":"12", "day_start": "30", "year_end": "2020", "month_end": "1", "day_end": "1",
#               "timezone": "eastern"}
# with_weather = commander.create_rep(False, True, True, True, True, True, parameters)

# -----------------------------------------------------
# Print weather rep
# for one_day in with_weather.one_days:
#     pprint.pprint(one_day)

# -----------------------------------------------------
# Print .CSV
csv = with_weather.get_csv(True, True, True, True, True, True, True)
print(csv)
file = open("Data/test_csv.csv", "w+")
file.write(csv)
file.close()
