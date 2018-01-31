# TODO: Error checking on importing from fields (and failing)
# TODO: grey out country parameter if any twilight data is not None
# TODO: add fix_dst option under complete_rep/the function within
# TODO: get rid of write_unfixed_dict and write_unfixed_dict with write_twilight (after fix_dst option implemented)

"""
All default (scrape all except for Astro and Civil
{'Weather': {'Action': 'Scrape'}, 'Parameters': {'City': 'Cambridge', 'State': 'MA', 'Country': 'US', 'Days': '14', 'weatherbit.io Key': 'a', 'Imperial Units': True, 'Save Weather': False, 'Apply Daylight Savings': True, 'Save Twilight': False}, 'Sun': {'Action': 'Scrape'}, 'Moon': {'Action': 'Scrape'}, 'Nautical': {'Action': 'Scrape'}, 'Astronomical': {'Action': 'None'}, 'Civil': {'Action': 'None'}}

Weather and Sun Import, others default
{'Weather': {'Action': 'Import', 'Path': 'a'}, 'Parameters': {'Apply Daylight Savings': True, 'Save Twilight': False}, 'Sun': {'Action': 'Import', 'Path': 'a'}, 'Moon': {'Action': 'Scrape'}, 'Nautical': {'Action': 'Scrape'}, 'Astronomical': {'Action': 'None'}, 'Civil': {'Action': 'None'}}

Weather and Sun None, others default
{'Weather': {'Action': 'None'}, 'Parameters': {'Date Start': '2018MAR28', 'Date End': '2018JUN28', 'City': 'Cambridge', 'State': 'MA', 'Timezone': 'Eastern', 'Apply Daylight Savings': True, 'Save Twilight': False}, 'Sun': {'Action': 'None'}, 'Moon': {'Action': 'Scrape'}, 'Nautical': {'Action': 'Scrape'}, 'Civil': {'Action': 'None'}, 'Astronomical': {'Action': 'None'}}
"""


def process_gathered(gathered_data):
    """
    Processes and formats data from commander.gather.gather_all into arguments for complete_rep.create_rep .
    In the case of importing data and invalid files/bad paths, will throw a pop-up and abort.
    :param gathered_data: from gather_all
    :return: arguments for create_rep or a pop-up showing the bad files.
    """
    parameters = translate_parameters(gathered_data["Parameters"])
    print(parameters)


def translate_parameters(gathered_parameters):
    """
    Converts parameters from gather_all into parameters compatible with complete_rep.
    :param gathered_parameters: value (dictionary) of "Parameters" from gather_all
    :return: dictionary {translated_key: same value, ...}
    """
    # The way gather_all works is it takes the labels from the GUI, which are human readable but decided after
    # complete_rep. Probably could've just edited all names within complete_rep but would've had to rewrite tests.
    # Performance isn't a huge deal so this is a quick fix.

    out = {"write_html": False, "write_unfixed_dict": False, }  # default values for all possible parameters from GUI
    translator = {"weatherbit.io Key": "api_key", "City": "city", "State": "state", "Days": "days",
                  "Imperial Units": "imperial_units", "Country": "Country", "Save Weather": "write_weather", "Apply Daylight Savings": "fix_dst",
                  "Timezone": "timezone", "Save Twilight": "write_fixed_dict",
                  "Date Start": "year_start", "Date End": "year_end"}
    # Date Start and Date End translations will be overwritten later, this is for iteration.

    for old_param in gathered_parameters.keys():
        out[translator[old_param]] = gathered_parameters[old_param]
        # basically just renaming the keys

    if "Date Start" in gathered_parameters.keys() and "Date End" in gathered_parameters.keys():
        out["year_start"], out["month_start"], out["day_start"] = date_to_components(gathered_parameters["Date Start"])
        out["year_end"], out["month_end"], out["day_end"] = date_to_components(gathered_parameters["Date End"])

    return out


def date_to_components(date):
    """
    Turns military date into its year, month, day components.
    :param date: e.g. "2017MAR28" for March 28, 2017.
    :return: tuple of components in year, month (number form), day order e.g. for above case: (2017, 03, 28)
    """
    year = date[:4]

    month_unconverted = date[4:7]
    converter = {"JAN": "1", "FEB": "2", "MAR": "3", "APR": "4", "MAY": "5", "JUN": "6", "JUL": "7", "AUG": "8",
                 "SEP": "9", "OCT": "10", "NOV": "11", "DEC": "12"}
    month = converter[month_unconverted]

    day = date[7:].lstrip("0")  # strip leading zero

    return year, month, day


def import_data(path):
    """

    :param path:
    :return:
    """
    pass
