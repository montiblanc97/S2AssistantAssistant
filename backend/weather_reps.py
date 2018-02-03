import datetime

from backend.exception import MissingDataError
from backend.twilight_scraper import next_day


class OneDayData:
    """
    Represents one day's data with any combination of general weather, sun data, moon data,
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
            self.__init_date(weather_data)

            self.high_temperature = str(weather_data["max_temp"])
            self.low_temperature = str(weather_data["min_temp"])
            self.overview = weather_data["weather"]["description"]
            self.precipitation = str(weather_data["pop"])
            self.humidity = str(weather_data["rh"])

            self.__init_wind(weather_data)
            self.__init_guidance()
        else:
            if year is None or month is None or day is None:
                raise Exception("Need either weather data or date")
            self.year = str(year)
            self.month = str(month).lstrip("0")
            self.day = str(day).lstrip("0")

        date = datetime.date(int(self.year), int(self.month), int(self.day))
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

        if sun_data is not None:
            self.sunrise = sun_data["data"][self.month][self.day]["sunrise"]
            self.sunset = sun_data["data"][self.month][self.day]["sunset"]

        if moon_data is not None:
            self.moonrise = moon_data["data"][self.month][self.day]["moonrise"]
            self.moonset = moon_data["data"][self.month][self.day]["moonset"]

        if nautical_twilight_data is not None:
            self.BMNT = nautical_twilight_data["data"][self.month][self.day]["BMNT"]
            self.EENT = nautical_twilight_data["data"][self.month][self.day]["EENT"]

        if civil_twilight_data is not None:
            self.BMCT = civil_twilight_data["data"][self.month][self.day]["BMCT"]
            self.EECT = civil_twilight_data["data"][self.month][self.day]["EECT"]

        if astronomical_twilight_data is not None:
            self.BMAT = astronomical_twilight_data["data"][self.month][self.day]["BMAT"]
            self.EEAT = astronomical_twilight_data["data"][self.month][self.day]["EEAT"]

    def __init_date(self, weather_data):
        date_data = weather_data["datetime"].split("-")  # [year, month, day]
        self.year = date_data[0]
        self.month = date_data[1].lstrip("0")
        self.day = date_data[2].lstrip("0")

        date = datetime.date(int(self.year), int(self.month), int(self.day))
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
        self.wind_speed = int(weather_data["wind_spd"])
        self.wind_direction = weather_data["wind_cdir"]

        if self.wind_speed >= high:
            self.wind_category = "High"
        elif self.wind_speed >= moderate:
            self.wind_category = "Moderate"
        else:
            self.wind_category = "Light"

        self.wind_speed = str(self.wind_speed)

    def __init_guidance(self):
        self.guidance_PT = "None"
        self.guidance_training = "None"
        self.guidance_driving = "None"

        lower = self.overview.lower()
        if "rain" in lower or "snow" in lower or "shower" in lower:
            if self.day_of_week in {"MON", "WED", "FRI"}:
                if "am" in lower or "morning" in lower:
                    self.guidance_PT = "High"
                if ("pm" in lower or "evening" in lower) and self.day_of_week == "WED":
                    self.guidance_training = "High"
                else:  # all day
                    self.guidance_PT = "High"
                    if self.day_of_week == "WED":
                        self.guidance_training = "High"

            self.guidance_driving = "High"


class MultiDayData:
    """
    Represents multi-day data with any combination of general weather, sun data, moon data,
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
                one_day_weather = OneDayData(weather_data=one_day_weather_data, sun_data=matched_sun_data,
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
                one_day_weather = OneDayData(weather_data=None, sun_data=matched_sun_data,
                                             moon_data=matched_moon_data,
                                             nautical_twilight_data=matched_nautical_twilight_data,
                                             civil_twilight_data=matched_civil_twilight_data,
                                             astronomical_twilight_data=matched_astronomical_twilight_data,
                                             year=year, month=month, day=day)
                self.one_days.append(one_day_weather)
                year, month, day = next_day(year, month, day)
        self.__mark_availability(weather_data, sun_data, moon_data,
                                 nautical_twilight_data, civil_twilight_data, astronomical_twilight_data)

    def __mark_availability(self, weather_data, sun_data, moon_data,
                            nautical_twilight_data, civil_twilight_data, astronomical_twilight_data):
        self.weather_available = True if weather_data is not None else False
        self.sun_available = True if sun_data is not None else False
        self.moon_available = True if moon_data is not None else False
        self.nautical_available = True if nautical_twilight_data is not None else False
        self.civil_available = True if civil_twilight_data is not None else False
        self.astronomical_available = True if astronomical_twilight_data is not None else False

    def __setup_twilight_data(self, sun_data, moon_data, nautical_twilight_data, civil_twilight_data,
                              astronomical_twilight_data):
        sun_data = self.__list_padding(sun_data)  # to support multiple years
        moon_data = self.__list_padding(moon_data)
        nautical_twilight_data = self.__list_padding(nautical_twilight_data)
        civil_twilight_data = self.__list_padding(civil_twilight_data)
        astronomical_twilight_data = self.__list_padding(astronomical_twilight_data)
        return sun_data, moon_data, nautical_twilight_data, civil_twilight_data, astronomical_twilight_data

    @staticmethod
    def __list_padding(data):
        """
        Puts data into a list if not already a list
        :param data:
        :return: data in a list if not already a list
        """
        if data is None:
            return None

        if type(data) is not list:
            return [data]

        else:
            return data

    @staticmethod
    def __match(list_twilight_data, year):
        """
        From a list of twilight data, return the data of a specific year or raise a MissingTwilightDataError otherwise
        :param list_twilight_data:
        :param year: to be looked up
        :return: twilight data for year or MissingDataError if not found
        """
        if list_twilight_data is None:
            return None

        for year_data in list_twilight_data:
            if year_data["year"] == year:
                return year_data

        raise MissingDataError("Twilight data missing required year")

    def get_csv(self, weather, sun, moon, nautical, civil, astronomical, guidance):
        """
        Returns string in .csv format for requested properties for all days.
        Days for each column, rows for each property. If data doesn't exist, it will be ignored.
        CSV tested working for Google Sheets, not working for Excel.
        :param weather: bool on whether or not to export weather data
        :param sun: "" for sun
        :param moon: "" for moon
        :param nautical: "" for nautical twilight
        :param civil: "" for civil twilight
        :param astronomical: "" for astronomical twilight
        :param guidance: "" for training guidance based on weather
        :return: string in .csv format
        """
        out = ""
        properties = ["date"]
        twilight_types = []

        if weather is True:
            if not self.weather_available:
                raise MissingDataError("Requested weather data for .csv but non-existent")
            properties.append("temperature")
            properties.append("overview")
            properties.append("precipitation/humidity")
            properties.append("wind")

        if sun is True:
            if not self.sun_available:
                raise MissingDataError("Requested sun data for .csv but non-existent")
            twilight_types.append("sun")
        if moon is True:
            if not self.moon_available:
                raise MissingDataError("Requested moon data for .csv but non-existent")
            twilight_types.append("moon")
        if nautical is True:
            if not self.nautical_available:
                raise MissingDataError("Requested nautical twilight data for .csv but non-existent")
            twilight_types.append("nautical")
        if civil is True:
            if not self.civil_available:
                raise MissingDataError("Requested civil twilight data for .csv but non-existent")
            twilight_types.append("civil")
        if astronomical is True:
            if not self.astronomical_available:
                raise MissingDataError("Requested astronomical twilight data for .csv but non-existent")
            twilight_types.append("astronomical")
        if len(twilight_types) > 0:
            properties.append("twilight")

        if guidance is True:
            properties.append("guidance_PT")
            properties.append("guidance_training")
            properties.append("guidance_driving")

        for prop in properties:
            out += self.csv_row(prop, twilight_types)

        return out

    def csv_row(self, prop, twilight_types=None):
        """
        Returns a row of property values for all days.
        :param prop: to look up
        :param twilight_types: if property is "twilight", a list of which are desired e.g. ["sun", "moon"]
        :return: string of that property for all days
        """
        out = ""
        cell_new_line = "\n"  # change for different editors
        if prop == "date":
            out += "Date,"
            # "MON\n12/25"
            for day in self.one_days:
                out += "\"" + day.day_of_week + cell_new_line + day.month + "/" + day.day + "\","
            return out + "\n"

        if prop == "temperature":
            out += "Temperature High/Low,"
            for day in self.one_days:
                out += "\"" + day.high_temperature + "/" + day.low_temperature + "\","
            return out + "\n"

        if prop == "precipitation/humidity":
            out += "\"Precipitation\nHumidity\","
            for day in self.one_days:
                out += "\"" + day.precipitation + "%" + cell_new_line + day.humidity + "%" + cell_new_line + "\","
            return out + "\n"

        if prop == "wind":
            out += "Wind,"
            for day in self.one_days:
                out += "\"" + day.wind_category + cell_new_line + day.wind_speed + "mph " + day.wind_direction + "\","
            return out + "\n"

        if prop == "twilight":
            twilight_lookup = {"sun": ["sunrise", "sunset"], "moon": ["moonrise", "moonset"],
                               "nautical": ["BMNT", "EENT"], "astronomical": ["BMAT", "EEAT"],
                               "civil": ["BMCT", "EECT"]}
            twilight_properties = []
            for twilight_type in twilight_types:
                twilight_properties.extend(twilight_lookup[twilight_type])

            out += "\""
            name_converter = {"sunrise": "SR", "sunset": "SS", "moonrise": "MR", "moonset": "MS"}
            for twilight_prop in twilight_properties:
                inter = twilight_prop
                if inter in name_converter:
                    inter = name_converter[inter]
                out += inter + "\n"
            out = out[:-1]  # ignore last new line
            out += "\","

            for day in self.one_days:
                inter = "\""
                for twilight_prop in twilight_properties:
                    inter += getattr(day, twilight_prop) + cell_new_line
                out += inter[:-1] + "\","  # ignore last new line
            return out + "\n"

        if prop == "guidance_PT":
            out += "PT,"
        elif prop == "guidance_training":
            out += "Training,"
        elif prop == "guidance_driving":
            out += "Driving,"
        else:
            out += prop.title() + ","  # can make for others but this is extent for Army ROTC slides

        for day in self.one_days:
            out += getattr(day, prop) + ","
        return out + "\n"
