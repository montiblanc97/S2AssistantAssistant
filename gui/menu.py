# parameters = {"api_key": "", "city": "Cambridge", "state": "MA", "days": "14", "write_weather": True,
#               "write_unfixed_dict": True, "write_fixed_dict": True, "imperial_units": True, "write_html": True}
# with_weather = commander.create_rep(True, True, True, True, True, True, parameters)

# parameters = {"city": "Cambridge", "state": "MA", "days": "14", "write_weather": True, "write_unfixed_dict": True,
#               "write_fixed_dict": True, "imperial_units": True, "write_html": True, "year_start": "2018",
#               "month_start":"12", "day_start": "30", "year_end": "2020", "month_end": "1", "day_end": "1",
#               "timezone": "eastern"}
# with_weather = commander.create_rep(False, True, True, True, True, True, parameters)


"""
Load data:
    (all radio buttons)
    -weather {scrape: city, state, country, api_key, days, imperial_units, save_weather_data} {load: browse} {None}
    -twilight_data {sun, moon, nautical, civil, astronomical}
        -panel for each setting, {scrape: fix_dst, save_*sun*_data
            if weather is not selected: city, state, timezone, year_start, etc. } {load: browse} {None}

Output data:
    - (checkboxes) include: {weather, sun, moon, nautical, civil, astronomical}
    - (textbox) output
"""

# change twilight scraper to have fix_dst option
