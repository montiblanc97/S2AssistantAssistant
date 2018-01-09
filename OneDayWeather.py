import datetime
from twilight_scraper import next_day

"""
example weather_data:
{
  "wind_cdir": "SW",
  "rh": 82,
  "wind_spd": 11.2,
  "pop": 15,
  "wind_cdir_full": "southwest",
  "slp": 1005.8,
  "app_max_temp": 45.1,
  "pres": 1002.5,
  "dewpt": 36,
  "snow": 0,
  "uv": 2,
  "ts": 1513684800,
  "wind_dir": 225,
  "weather": {
    "icon": "c04d",
    "code": "804",
    "description": "Overcast clouds"
  },
  "app_min_temp": 25.4,
  "max_temp": 45.1,
  "snow_depth": 0,
  "precip": 0,
  "max_dhi": 252.8,
  "datetime": "2017-12-19",
  "temp": 41,
  "min_temp": 33.8,
  "clouds": 93,
  "vis": 6.2
}
"""


class OneDayWeather:
    """
    Represents one day's weather data with any combination of general weather, sun data, moon data,
    nautical twilight times, civil twilight times, and astronomical twilight times.
    """

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))

    def __init__(self, weather_data=None, sun_data=None, moon_data=None,
                 nautical_twilight_data=None, civil_twilight_data=None, astronomical_twilight_data=None,
                 year=None, month=None, day=None):
        if weather_data is not None:
            self.weather_available = True
            self.__init_date(weather_data)

            self.high_temperature = weather_data["max_temp"]
            self.low_temperature = weather_data["min_temp"]
            self.overview = weather_data["weather"]["description"]
            self.precipitation = weather_data["pop"]
            self.humidity = weather_data["rh"]

            self.__init_wind(weather_data)
            self.__init_guidance()
        else:
            if year is None or month is None or day is None:
                raise Exception("Need either weather data or date")
            self.weather_available = False
            self.year = str(year)
            self.month = str(month).lstrip("0")
            self.day = str(day).lstrip("0")

        if sun_data is not None:
            self.sun_available = True
            self.sunrise = sun_data["data"][self.month][self.day]["sunrise"]
            self.sunset = sun_data["data"][self.month][self.day]["sunset"]
        else:
            self.sun_available = False

        if moon_data is not None:
            self.moon_available = True
            self.moonrise = moon_data["data"][self.month][self.day]["moonrise"]
            self.moonset = moon_data["data"][self.month][self.day]["moonset"]
        else:
            self.moon_available = False

        if nautical_twilight_data is not None:
            self.nautical_twilight_available = True
            self.BMNT = nautical_twilight_data["data"][self.month][self.day]["BMNT"]
            self.EENT = nautical_twilight_data["data"][self.month][self.day]["EENT"]
        else:
            self.nautical_twilight_available = False

        if civil_twilight_data is not None:
            self.civil_twilight_available = True
            self.BMCT = civil_twilight_data["data"][self.month][self.day]["BMCT"]
            self.EECT = civil_twilight_data["data"][self.month][self.day]["EECT"]
        else:
            self.civil_twilight_available = False

        if nautical_twilight_data is not None:
            self.astronomical_twilight_available = True
            self.BMAT = astronomical_twilight_data["data"][self.month][self.day]["BMAT"]
            self.EEAT = astronomical_twilight_data["data"][self.month][self.day]["EEAT"]
        else:
            self.astronomical_twilight_available = False

    def __init_date(self, weather_data):
        date_data = weather_data["datetime"].split("-")  # [year, month, day]
        self.year = date_data[0]
        self.month = date_data[1].lstrip("0")
        self.day = date_data[2].lstrip("0")

        date = datetime.date(int(date_data[0]), int(date_data[1]), int(date_data[2]))
        day_of_week_lookup = {
            0: "MON",
            1: "TUE",
            2: "WED",
            3: "THU",
            4: "FRI",
            5: "SAT",
            6: "SUN"
        }
        self.day_of_week = day_of_week_lookup[date.weekday()]

    def __init_wind(self, weather_data, moderate=11, high=17):
        self.wind_speed = weather_data["wind_spd"]
        self.wind_direction = weather_data["wind_cdir"]

        if self.wind_speed >= high:
            self.wind_category = "High"
        elif self.wind_speed >= moderate:
            self.wind_category = "Moderate"
        else:
            self.wind_category = "Light"

    def __init_guidance(self):
        self.guidance_PT = "None"
        self.guidance_training = "None"
        self.guidance_driving = "None"

        lower = self.overview.lower()
        if "rain" in lower or "snow" in lower or "shower" in lower:

            if "am" in lower and self.day_of_week in {"MON", "WED", "FRI"}:
                self.guidance_PT = "High"
            if "pm" in lower and self.day_of_week == "WED":
                self.guidance_training = "High"
            self.guidance_driving = "High"


class MultiDayWeather:
    """
    Represents multi-day weather data with any combination of general weather, sun data, moon data,
    nautical twilight times, civil twilight times, and astronomical twilight times.
    """

    def __str__(self):
        return str(self.one_days)

    def __repr__(self):
        return str(self.one_days)

    def __init__(self, weather_data=None, sun_data=None, moon_data=None,
                 nautical_twilight_data=None, civil_twilight_data=None, astronomical_twilight_data=None,
                 year_start=None, month_start=None, day_start=None,
                 year_end=None, month_end=None, day_end=None):
        sun_data, moon_data, nautical_twilight_data, civil_twilight_data, astronomical_twilight_data = \
            self.__setup_twilight_data(sun_data, moon_data, nautical_twilight_data, civil_twilight_data,
                                       astronomical_twilight_data)
        self.one_days = []
        if weather_data is not None:
            for one_day_weather_data in weather_data["data"]:
                matched_sun_data = self.__match(sun_data, one_day_weather_data["datetime"][0:4])
                matched_moon_data = self.__match(moon_data, one_day_weather_data["datetime"][0:4])
                matched_nautical_twilight_data = self.__match(nautical_twilight_data,
                                                              one_day_weather_data["datetime"][0:4])
                matched_civil_twilight_data = self.__match(civil_twilight_data,
                                                           one_day_weather_data["datetime"][0:4])
                matched_astronomical_twilight_data = self.__match(astronomical_twilight_data,
                                                                  one_day_weather_data["datetime"][0:4])
                one_day_weather = OneDayWeather(weather_data=one_day_weather_data, sun_data=matched_sun_data,
                                                moon_data=matched_moon_data,
                                                nautical_twilight_data=matched_nautical_twilight_data,
                                                civil_twilight_data=matched_civil_twilight_data,
                                                astronomical_twilight_data=matched_astronomical_twilight_data)
                self.one_days.append(one_day_weather)
        else:
            if year_start is None or month_start is None or day_start is None or \
                    year_end is None or month_end is None or day_end is None:
                raise Exception("Need either weather data or date")

            year, month, day = year_start, month_start, day_start
            year_end, month_end, day_end = next_day(year_end, month_end, day_end)  # to be inclusive
            while (year, month, day) != (year_end, month_end, day_end):
                matched_sun_data = self.__match(sun_data, year)
                matched_moon_data = self.__match(moon_data, year)
                matched_nautical_twilight_data = self.__match(nautical_twilight_data, year)
                matched_civil_twilight_data = self.__match(civil_twilight_data, year)
                matched_astronomical_twilight_data = self.__match(astronomical_twilight_data, year)
                one_day_weather = OneDayWeather(weather_data=None, sun_data=matched_sun_data,
                                                moon_data=matched_moon_data,
                                                nautical_twilight_data=matched_nautical_twilight_data,
                                                civil_twilight_data=matched_civil_twilight_data,
                                                astronomical_twilight_data=matched_astronomical_twilight_data,
                                                year=year, month=month, day=day)
                self.one_days.append(one_day_weather)
                year, month, day = next_day(year, month, day)

    def __setup_twilight_data(self, sun_data, moon_data, nautical_twilight_data, civil_twilight_data,
                              astronomical_twilight_data):
        sun_data = self.__list_padding(sun_data)  # to support multiple years
        moon_data = self.__list_padding(moon_data)
        nautical_twilight_data = self.__list_padding(nautical_twilight_data)
        civil_twilight_data = self.__list_padding(civil_twilight_data)
        astronomical_twilight_data = self.__list_padding(astronomical_twilight_data)
        return sun_data, moon_data, nautical_twilight_data, civil_twilight_data, astronomical_twilight_data

    def __list_padding(self, data):
        if data is None:
            return None

        if type(data) is not list:
            return [data]

        else:
            return data

    def __match(self, twilight_data, year):
        if twilight_data is None:
            return None

        for year_data in twilight_data:
            if year_data["year"] == year:
                return year_data

        raise Exception("Corresponding year not found")

    def get_csv(self):
        pass
