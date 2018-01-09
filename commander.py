import OneDayWeather
import twilight_scraper
import weatherbit_caller
from exception import AccessError


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
                                          if twilight data also needed: "country"
            keys needed for twilight data: "city", "state", "write_html", "write_unfixed_dict", "write_fixed_dict",
                                          if weather data is not given/scraped: "timezone", "year_start", "month_start",
                                                                                "day_start", "year_end", "month_end",
                                                                                "day_end"
    :return: MultiDayWeather object representing passed/scraped data
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
        return OneDayWeather.MultiDayWeather(weather, sun, moon, nautical, civil, astronomical, year_start, month_start,
                                             day_start, year_end, month_end, day_end)
    else:
        return OneDayWeather.MultiDayWeather(weather, sun, moon, nautical, civil, astronomical)


def classifier(task_name, parameters, weather=None):
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
        city = error_catch_access("city", parameters)
        state = error_catch_access("state", parameters)
        write_html = error_catch_access("write_html", parameters)
        write_unfixed_dict = error_catch_access("write_unfixed_dict", parameters)
        write_fixed_dict = error_catch_access("write_fixed_dict", parameters)

        if weather is None:
            timezone = error_catch_access("timezone", parameters)

            out = []
            year_start = error_catch_access("year_start", parameters)
            month_start = error_catch_access("month_start", parameters)
            day_start = error_catch_access("day_start", parameters)
            year_end = error_catch_access("year_end", parameters)
            month_end = error_catch_access("month_end", parameters)
            day_end = error_catch_access("day_end", parameters)

            years_needed = [year_start]
            current = int(year_start)
            while current != int(year_end):
                current += 1
                years_needed.append(str(current))

            for year in years_needed:
                out.append(twilight_scraper.twilight_scrape_fix(task_name, year, city, state, timezone,
                                                                write_html, write_unfixed_dict,
                                                                write_fixed_dict))
            return out
        else:
            out = []
            years_needed = weatherbit_caller.get_years(weather)
            for year in years_needed:
                out.append(twilight_scraper.twilight_scrape_fix_auto_timezone(task_name, year, city, state, weather,
                                                                              write_html, write_unfixed_dict,
                                                                              write_fixed_dict))
            return out


def error_catch_access(key, parameters):
    if key not in parameters.keys():
        raise AccessError("Required parameter: " + key + " not found")
    return parameters[key]
