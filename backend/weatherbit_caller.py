import datetime
import json

import requests
import os, errno

def write_city_weather_data(api_key, city="Cambridge", state="MA", country="US",
                            days="14", imperial_units=True, write=True):
    """
    Gets weather data via weatherbit API, writes and returns data as dict
    :param api_key: weatherbit API developer key
    :param city: of interest
    :param state: of interest, can be initials or full name
    :param country: of interest, must be two letter initials
    :param days: how many days forecast to read (max 16)
    :param imperial_units: true for Imperial Units, false for Metric
    :param write: path to save .json weather data or True to save in ./Data directory
    :return: dict of weather data
    side effect: saves data in .json if parameter write is True
    """
    url = "https://api.weatherbit.io/v2.0/forecast/daily"

    url += "?key=" + api_key
    url += "&lang=en"

    state = state.replace(" ", "+")  # tate can be spelled out "North Dakota" but for purposes of URL creation
    city = city.replace(" ", "+")
    url += "&city=" + city + "," + state
    url += "&country=" + country

    url += "&days=" + days
    url += "&units=" + "I" if imperial_units else "M"

    response = requests.get(url)

    if write:
        try:  # create directory if doesn't exist
            os.makedirs("Data")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # to save date gathered (only daily weather requested)
        now = datetime.datetime.now()
        if type(write) is str:  # some sort of path given
            if "." in write:  # path to file given
                filename = write
            else:  # path to directory given
                filename = write + "/weather_data_%s_%s_%s.json" % (now.year, now.month, now.day)
        else:  # True
            filename = "Data/weather_data_%s_%s_%s.json" % (now.year, now.month, now.day)

        writing = open(filename, "w+")
        writing.write(response.text)
        writing.close()

    return json.loads(response.text)


"""
example output:
{
  "data": [
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
    },
    {
      "wind_cdir": "SW",
      "rh": 60,
      "wind_spd": 13.4,
      "pop": 15,
      "wind_cdir_full": "southwest",
      "slp": 1009.2,
      "app_max_temp": 34.3,
      "pres": 1005.7,
      "dewpt": 23,
      "snow": 0.1,
      "uv": 3,
      "ts": 1513771200,
      "wind_dir": 225,
      "weather": {
        "icon": "c02d",
        "code": "802",
        "description": "Scattered clouds"
      },
      "app_min_temp": 18.1,
      "max_temp": 41.5,
      "snow_depth": 0.1,
      "precip": 0,
      "max_dhi": 622.8,
      "datetime": "2017-12-20",
      "temp": 35.6,
      "min_temp": 28.8,
      "clouds": 17,
      "vis": 6.2
    },
    {
      "wind_cdir": "SW",
      "rh": 43,
      "wind_spd": 6.7,
      "pop": 0,
      "wind_cdir_full": "southwest",
      "slp": 1021.8,
      "app_max_temp": 25.1,
      "pres": 1018.2,
      "dewpt": 8.8,
      "snow": 0,
      "uv": 5,
      "ts": 1513857600,
      "wind_dir": 225,
      "weather": {
        "icon": "c01d",
        "code": "800",
        "description": "Clear sky"
      },
      "app_min_temp": 16.4,
      "max_temp": 31.5,
      "snow_depth": 0.1,
      "precip": 0,
      "max_dhi": 705.6,
      "datetime": "2017-12-21",
      "temp": 28.4,
      "min_temp": 24.3,
      "clouds": 0,
      "vis": 6.2
    },
    {
      "wind_cdir": "ESE",
      "rh": 61,
      "wind_spd": 2.2,
      "pop": 45,
      "wind_cdir_full": "east-southeast",
      "slp": 1029.9,
      "app_max_temp": 33.1,
      "pres": 1026.3,
      "dewpt": 18.3,
      "snow": 1.1,
      "uv": 2,
      "ts": 1513944000,
      "wind_dir": 117,
      "weather": {
        "icon": "s02d",
        "code": "601",
        "description": "Snow"
      },
      "app_min_temp": 23.5,
      "max_temp": 34.3,
      "snow_depth": 1.2,
      "precip": 0.2,
      "max_dhi": 330.7,
      "datetime": "2017-12-22",
      "temp": 30.2,
      "min_temp": 25.7,
      "clouds": 77,
      "vis": 2.5
    },
    {
      "wind_cdir": "SE",
      "rh": 94,
      "wind_spd": 6.7,
      "pop": 15,
      "wind_cdir_full": "southeast",
      "slp": 1018.8,
      "app_max_temp": 59,
      "pres": 1014.7,
      "dewpt": 44.8,
      "snow": 0.2,
      "uv": 2,
      "ts": 1514030400,
      "wind_dir": 135,
      "weather": {
        "icon": "c04d",
        "code": "804",
        "description": "Overcast clouds"
      },
      "app_min_temp": 25.7,
      "max_temp": 59,
      "snow_depth": 1.4,
      "precip": 1.1,
      "max_dhi": 218.7,
      "datetime": "2017-12-23",
      "temp": 46.4,
      "min_temp": 32,
      "clouds": 100,
      "vis": 4.3
    },
    {
      "wind_cdir": "SW",
      "rh": 64,
      "wind_spd": 6.7,
      "pop": 15,
      "wind_cdir_full": "southwest",
      "slp": 1018.8,
      "app_max_temp": 59,
      "pres": 1015.1,
      "dewpt": 29.8,
      "snow": 0,
      "uv": 2,
      "ts": 1514116800,
      "wind_dir": 225,
      "weather": {
        "icon": "c03d",
        "code": "803",
        "description": "Broken clouds"
      },
      "app_min_temp": 31.1,
      "max_temp": 59,
      "snow_depth": 0.7,
      "precip": 0,
      "max_dhi": 335.6,
      "datetime": "2017-12-24",
      "temp": 41,
      "min_temp": 36.5,
      "clouds": 76,
      "vis": 6.2
    },
    {
      "wind_cdir": "SW",
      "rh": 82,
      "wind_spd": 4.5,
      "pop": 55,
      "wind_cdir_full": "southwest",
      "slp": 1016.3,
      "app_max_temp": 34.5,
      "pres": 1012.9,
      "dewpt": 27.1,
      "snow": 1.9,
      "uv": 2,
      "ts": 1514203200,
      "wind_dir": 225,
      "weather": {
        "icon": "s03d",
        "code": "601",
        "description": "Snow"
      },
      "app_min_temp": 21.3,
      "max_temp": 37.9,
      "snow_depth": 2.6,
      "precip": 0.3,
      "max_dhi": 272.3,
      "datetime": "2017-12-25",
      "temp": 32,
      "min_temp": 26.6,
      "clouds": 89,
      "vis": 2.5
    },
    {
      "wind_cdir": "SW",
      "rh": 64,
      "wind_spd": 8.9,
      "pop": 15,
      "wind_cdir_full": "southwest",
      "slp": 1018.3,
      "app_max_temp": 30.5,
      "pres": 1014.7,
      "dewpt": 19.4,
      "snow": 0.1,
      "uv": 3,
      "ts": 1514289600,
      "wind_dir": 225,
      "weather": {
        "icon": "c02d",
        "code": "802",
        "description": "Scattered clouds"
      },
      "app_min_temp": 14.3,
      "max_temp": 37,
      "snow_depth": 2.7,
      "precip": 0,
      "max_dhi": 535.2,
      "datetime": "2017-12-26",
      "temp": 30.2,
      "min_temp": 23.9,
      "clouds": 35,
      "vis": 6.2
    },
    {
      "wind_cdir": "SW",
      "rh": 42,
      "wind_spd": 15.7,
      "pop": 15,
      "wind_cdir_full": "southwest",
      "slp": 1031.4,
      "app_max_temp": 16,
      "pres": 1028,
      "dewpt": 0,
      "snow": 0,
      "uv": 4,
      "ts": 1514376000,
      "wind_dir": 225,
      "weather": {
        "icon": "c01d",
        "code": "800",
        "description": "Clear sky"
      },
      "app_min_temp": -2.5,
      "max_temp": 27.9,
      "snow_depth": 2.7,
      "precip": 0,
      "max_dhi": 676.4,
      "datetime": "2017-12-27",
      "temp": 19.4,
      "min_temp": 13.5,
      "clouds": 6,
      "vis": 6.2
    },
    {
      "wind_cdir": "SW",
      "rh": 36,
      "wind_spd": 4.5,
      "pop": 0,
      "wind_cdir_full": "southwest",
      "slp": 1040,
      "app_max_temp": 15.4,
      "pres": 1036.4,
      "dewpt": -6.5,
      "snow": 0,
      "uv": 4,
      "ts": 1514462400,
      "wind_dir": 225,
      "weather": {
        "icon": "c01d",
        "code": "800",
        "description": "Clear sky"
      },
      "app_min_temp": 1.8,
      "max_temp": 21.6,
      "snow_depth": 2.7,
      "precip": 0,
      "max_dhi": 681.3,
      "datetime": "2017-12-28",
      "temp": 15.8,
      "min_temp": 9.9,
      "clouds": 5,
      "vis": 6.2
    },
    {
      "wind_cdir": "S",
      "rh": 54,
      "wind_spd": 4.5,
      "pop": 45,
      "wind_cdir_full": "south",
      "slp": 1031.5,
      "app_max_temp": 29.3,
      "pres": 1027.9,
      "dewpt": 8.8,
      "snow": 1.2,
      "uv": 2,
      "ts": 1514548800,
      "wind_dir": 180,
      "weather": {
        "icon": "s02d",
        "code": "601",
        "description": "Snow"
      },
      "app_min_temp": 10.8,
      "max_temp": 33.4,
      "snow_depth": 3.9,
      "precip": 0.2,
      "max_dhi": 267.4,
      "datetime": "2017-12-29",
      "temp": 23,
      "min_temp": 17.6,
      "clouds": 90,
      "vis": 2.5
    },
    {
      "wind_cdir": "SW",
      "rh": 78,
      "wind_spd": 17.9,
      "pop": 15,
      "wind_cdir_full": "southwest",
      "slp": 999.5,
      "app_max_temp": 46.9,
      "pres": 995.8,
      "dewpt": 25.9,
      "snow": 0.1,
      "uv": 2,
      "ts": 1514635200,
      "wind_dir": 225,
      "weather": {
        "icon": "c03d",
        "code": "803",
        "description": "Broken clouds"
      },
      "app_min_temp": 13.6,
      "max_temp": 46.9,
      "snow_depth": 3.9,
      "precip": 0.2,
      "max_dhi": 369.7,
      "datetime": "2017-12-30",
      "temp": 32,
      "min_temp": 26.6,
      "clouds": 69,
      "vis": 6.2
    },
    {
      "wind_cdir": "SW",
      "rh": 58,
      "wind_spd": 13.4,
      "pop": 0,
      "wind_cdir_full": "southwest",
      "slp": 1021.8,
      "app_max_temp": 14.6,
      "pres": 1018,
      "dewpt": 3.6,
      "snow": 0,
      "uv": 4,
      "ts": 1514721600,
      "wind_dir": 225,
      "weather": {
        "icon": "c01d",
        "code": "800",
        "description": "Clear sky"
      },
      "app_min_temp": -1.8,
      "max_temp": 26.1,
      "snow_depth": 3.9,
      "precip": 0,
      "max_dhi": 676.4,
      "datetime": "2017-12-31",
      "temp": 15.8,
      "min_temp": 13.1,
      "clouds": 6,
      "vis": 6.2
    },
    {
      "wind_cdir": "SE",
      "rh": 70,
      "wind_spd": 2.2,
      "pop": 0,
      "wind_cdir_full": "southeast",
      "slp": 1025.5,
      "app_max_temp": 27.9,
      "pres": 1021.5,
      "dewpt": 14.7,
      "snow": 0,
      "uv": 3,
      "ts": 1514808000,
      "wind_dir": 135,
      "weather": {
        "icon": "c02d",
        "code": "802",
        "description": "Scattered clouds"
      },
      "app_min_temp": 9.6,
      "max_temp": 29.7,
      "snow_depth": 3.9,
      "precip": 0,
      "max_dhi": 598.5,
      "datetime": "2018-01-01",
      "temp": 23,
      "min_temp": 13.1,
      "clouds": 22,
      "vis": 6.2
    }
  ],
  "city_name": "Cambridge",
  "lon": "-71.10561",
  "timezone": "America\/New_York",
  "lat": "42.3751",
  "country_code": "US",
  "state_code": "MA"
}
"""
