import time

import backend.twilight_scraper as twilight_scraper
import backend.weather_reps as weather_reps
from backend.exception import AccessError, WeatherError

from backend import weatherbit_caller


def create_rep(weather=None, sun=None, moon=None, nautical=None, astronomical=None, civil=None, parameters=None):
    """
    Creates a representation of weather using previous data passed in or specified in parameters.
    :param weather: old data processed through this program or True to scrape, otherwise False or None
    :param sun: old data processed through this program or True to scrape, otherwise False or None
    :param moon: old data processed through this program or True to scrape, otherwise False or None
    :param nautical: old data processed through this program or True to scrape, otherwise False or None
    :param astronomical: old data processed through this program or True to scrape, otherwise False or None
    :param civil: old data processed through this program or True to scrape, otherwise False or None
    :param parameters: needed to scrape in a dictionary format {string: string or Boolean depending on key},
                       see specification for weather and twilight scrapers for details.
            keys needed for weather data: "api_key", "city", "state", "days", "imperial_units", "write_weather"
                                          if twilight data not needed: "country"
            keys needed for twilight data: "apply_dst", "write_twilight",
                                          if weather data is not given/scraped: "city", "state", "timezone",
                                                                                "year_start", "month_start",
                                                                                "day_start", "year_end", "month_end",
                                                                                "day_end"
    :return: MultiDayWeather object representing passed/scraped data, AccessError if required parameter not found
    """
    if weather is False:
        weather = None

    if parameters is None:
        parameters = {}

    if weather is True:
        weather = classifier("weather", parameters)

    if sun is True:
        sun = classifier("sun", parameters, weather)

    if moon is True:
        moon = classifier("moon", parameters, weather)

    if nautical is True:
        nautical = classifier("nautical twilight", parameters, weather)

    if civil is True:
        civil = classifier("civil twilight", parameters, weather)

    if astronomical is True:
        astronomical = classifier("astronomical twilight", parameters, weather)

    if weather is None:
        year_start = error_catch_access("year_start", parameters)
        month_start = error_catch_access("month_start", parameters)
        day_start = error_catch_access("day_start", parameters)
        year_end = error_catch_access("year_end", parameters)
        month_end = error_catch_access("month_end", parameters)
        day_end = error_catch_access("day_end", parameters)
        return weather_reps.MultiDayData(weather, sun, moon, nautical, civil, astronomical, year_start, month_start,
                                         day_start, year_end, month_end, day_end)
    else:
        return weather_reps.MultiDayData(weather, sun, moon, nautical, civil, astronomical)


def classifier(task_name, parameters, weather=None):
    """
    Scrapes weather or twilight data.
    :param task_name: "weather" or twilight task_names ("sun", "moon", etc.)
    :param parameters: necessary parameters needed, see create_rep specification
    :param weather: weather data (can be used instead of certain parameters, see create_rep specification)
    :return: relevant weather or twilight data, AccessError if required parameter not found
    """
    if task_name == "weather":
        api_key = error_catch_access("api_key", parameters)
        city = error_catch_access("city", parameters)
        state = error_catch_access("state", parameters)

        try:
            country = error_catch_access("country", parameters)
        except AccessError:
            country = "US"

        days = error_catch_access("days", parameters)
        imperial_units = error_catch_access("imperial_units", parameters)
        write_weather = error_catch_access("write_weather", parameters)
        return weatherbit_caller.write_city_weather_data(api_key, city, state, country, days, imperial_units,
                                                         write_weather)

    else:  # twilight data
        write_twilight = error_catch_access("write_twilight", parameters)
        apply_dst = error_catch_access("apply_dst", parameters)

        if weather is None:
            timezone = error_catch_access("timezone", parameters)
            city = error_catch_access("city", parameters)
            state = error_catch_access("state", parameters)

            out = []
            year_start = error_catch_access("year_start", parameters)
            year_end = error_catch_access("year_end", parameters)

            years_needed = [year_start]
            current = int(year_start)
            while current != int(year_end):
                current += 1
                years_needed.append(str(current))

            for year in years_needed:
                out.append(twilight_scraper.twilight_scrape(task_name, year, city, state, timezone, apply_dst,
                                                                write_twilight))
                time.sleep(2)  # don't scrape so fast
            return out
        else:
            out = []
            years_needed = get_years(weather)
            for year in years_needed:
                out.append(twilight_scraper.twilight_scrape_auto_weather(task_name, year, weather, apply_dst,
                                                                         write_twilight))
                time.sleep(2)  # don't scrape so fast
            return out


def error_catch_access(key, parameters):
    """
    Finds value associated with key in parameters or throws AccessError
    :param key: to be looked up
    :param parameters: dictionary to look up key in
    :return: value associated with key or AccessError if not found
    """
    if key not in parameters.keys():
        raise AccessError("Required parameter: " + key + " not found")
    return parameters[key]


def get_years(weather_data):
    """
    Using weather data from write_city_weather_data, determine the years of the days within.
    :param weather_data: from write_city_weather_data
    :return: list of years contained within weather_data
    """
    if weather_data is None or "data" not in weather_data:
        raise WeatherError("Year information not found")
    out = set()
    for day in weather_data["data"]:
        out.add(day["datetime"][:4])
    return list(out)
