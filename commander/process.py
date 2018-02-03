from json.decoder import JSONDecodeError
from json import loads
from commander.helpers import bad_popup


def process_gathered(gathered_data):
    """
    Processes and formats data from commander.gather.gather_all into arguments for complete_rep.create_rep .
    In the case of importing data and invalid files/bad paths, will throw a pop-up and False.
    :param gathered_data: from gather_all
    :return: arguments for create_rep or a pop-up showing the bad files and False.
    """
    out = []
    for data_type in ["Weather", "Sun", "Moon", "Nautical", "Astronomical", "Civil"]:
        try:
            out.append(classifier(gathered_data[data_type]))
        except ValueError:
            bad_popup(data_type + " Data could not be parsed")
            return False
        except FileNotFoundError:
            bad_popup(data_type + " Data not found at path")
            return False

    parameters = translate_parameters(gathered_data["Parameters"])
    out.append(parameters)

    return out


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
                  "Imperial Units": "imperial_units", "Country": "Country", "Save Weather": "write_weather",
                  "Apply Daylight Savings": "apply_dst", "Timezone": "timezone", "Save Twilight": "write_twilight",
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


def classifier(data_type):
    """
    From a given data type field (weather, sun, nautical, etc.), returns the proper parameter for create_rep.
    In the case of importing data, invalid files will cause JSONDecodeError and bad paths will throw
    FileNotFoundException
    :param data_type: the value of a data type from gather_all such as "Sun", "Moon".
            Will always contain {"Action": "Scrape" or "Import" or "None", "Path": path if Action is Import}
    :return: True for "Scrape", None for "None", and the loaded data for "Import" (or respective exception)
    """
    if "Action" not in data_type.keys():
        raise ValueError("data_type needs key Action" )

    action = data_type["Action"]

    if action == "Scrape":
        return True
    elif action == "None":
        return None
    elif action == "Import":
        if "Path" not in data_type.keys():
            raise ValueError("tried to import without a Path key in data_type")
        try:
            return import_data(data_type["Path"])
        except FileNotFoundError:
            raise FileNotFoundError("Invalid path: " + data_type["Path"])
        except ValueError:
            raise ValueError("Invalid file: " + data_type["Path"])
        # except can't load error
    else:
        raise ValueError("Action key doesn't have valid value, got: " + str(action))


def import_data(path):
    """
    Imports data from path. In the case of importing data, invalid files will cause JSONDecodeError and bad paths will
    throw FileNotFoundException
    :param path: of data
    :return: loaded data (or respective exception)
    """
    try:
        data = loads(open(path, "r+").read())
    except FileNotFoundError:
        raise FileNotFoundError("Invalid path: " + path)
    except JSONDecodeError:
        raise ValueError("Invalid file: " + path)
    return data

# import_data("E:\Desktop\Andrew\Google Drive\\2017-2018\sandbox\S2AssistantAssistant\\commander\\run.py")
