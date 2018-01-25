

def gather_all(main_menu):
    """
    From main_menu, determines necessary actions (scrape, import, none) for weather and twilight. Gathers corresponding
    data for said action, while validating correct parameter input. In case of incorrect parameter input, stops and
    notifies user via the GUI.
    :param main_menu: GUI window
    :return: all information necessary to run create_rep or nothing and mutates GUI to show incorrect input
    """
    gather_weather(main_menu.input.weather)
    gather_twilight(main_menu.input.twilight)


def gather_weather(weather_input):
    """
    Helper for gather_all, specific to weather information.
    :param weather_input: GUI window
    :return: all information necessary to run create_rep regarding weather or an error flag with missing/bad info
            (does not raise an exception or error)
    """
    out = {"weather": {"action": None, "parameters": {}}}

    action = weather_input.selector_button_group.checkedButton().text()  # "Scrape", "Import", or "None"
    func_map = {"Scrape": gather_weather_scrape, "Import": gather_weather_import, "None": gather_weather_none}

    out["weather"]["action"] = action

def gather_weather_scrape(weather_input):
    """
    Helper for gather_weather, specific to scrape option.
    :param weather_input: GUI window
    :return: boolean flag if input is valid and dict of all valid parameters to scrape weather or missing parameters
    """

def gather_twilight(twilight_input):
    """
    Helper for gather_all, specific to twilight information.
    :param twilight_input: GUI window
    :return: all information necessary to run create_rep regarding twilight or an error flag with missing/bad info
            (does not raise an exception or error)
    """
    pass