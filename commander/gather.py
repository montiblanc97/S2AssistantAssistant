from PyQt5.QtWidgets import QLineEdit, QCheckBox, QMessageBox

from commander.helpers import missing_popup


def gather_all(main_menu):
    """
    From main_menu, determines necessary actions (scrape, import, none) for weather and twilight. Gathers corresponding
    data for said action, while validating correct parameter input. In case of incorrect parameter input, stops and
    notifies user via the GUI.
    :param main_menu: GUI window that will be marked with incorrect input
    :return: if valid, True and all information necessary to run create_rep. Else, False and empty dict.
    """
    weather_flag, weather_data = gather_weather(main_menu.input.weather)
    twilight_flag, twilight_data = gather_twilight(main_menu.input.twilight)

    if weather_flag is False or twilight_flag is False:
        missing_popup("See red bordered fields.")
        return False, {}

    out = weather_data
    if weather_data["Weather"]["Action"] == "None":
        out.update(twilight_data)  # twilight types has everything needed
    else:  # Scrape or Import
        for twilight_type in ["Sun", "Moon", "Nautical", "Astronomical", "Civil"]:
            out[twilight_type] = twilight_data[twilight_type]
        out["Parameters"]["Apply Daylight Savings"] = twilight_data["Parameters"]["Apply Daylight Savings"]
        out["Parameters"]["Save Twilight"] = twilight_data["Parameters"]["Save Twilight"]

    return True, out


def gather_weather(weather_input):
    """
    Helper for gather_all, specific to weather information.
    :param weather_input: GUI window that will be marked with incorrect input
    :return: if valid, True and all information necessary to run create_rep regarding weather. Else, False
    """
    out = {"Weather": {"Action": None}, "Parameters": {}}

    action = weather_input.selector_button_group.checkedButton().text()  # "Scrape", "Import", or "None"
    func_map = {"Scrape": gather_weather_scrape, "Import": gather_weather_import, "None": gather_weather_none}

    func_map[action](weather_input)
    flag, parameters = func_map[action](weather_input)

    if flag is False:
        return False, {}
    else:
        out["Weather"]["Action"] = action
        if action == "Import":
            out["Weather"]["Path"] = parameters["Path"]
        else:
            out["Parameters"] = parameters
        return True, out


def gather_weather_scrape(weather_input):
    """
    Helper for gather_weather, specific to scrape option.
    :param weather_input: GUI window that will be marked with incorrect input
    :return: if valid, True and dictionary {parameter name: value} for weather scraping. Else, False and empty dict.
    """
    parameters = {}
    missing = []

    for key in weather_input.scrape_fields.keys():
        field_type = type(weather_input.scrape_fields[key])

        if field_type is QLineEdit:
            text = weather_input.scrape_fields[key].text()
            if text == "":  # very basic validity checking, TODO: validate each field against specific REGEX
                missing.append(key)
                weather_input.scrape_fields[key].setStyleSheet(weather_input.error_border)  # set red border around
            else:
                weather_input.scrape_fields[key].setStyleSheet(weather_input.default_border)  # set back if fixed later
            parameters[key] = text

        elif field_type is QCheckBox:
            parameters[key] = weather_input.scrape_fields[key].isChecked()
        else:
            raise TypeError("During weather scrape, found unknown form type: " + str(field_type))

    if len(missing) > 0:  # some parameters are missing
        return False, {}

        # error_text = ""
        # for param in missing:
        #     error_text += str(param) + ", "
        # error_text = error_text[:-2]  # strip of last comma and space
        # missing_popup(error_text)
    return True, parameters


def gather_weather_import(weather_input):
    """
    Helper for gather_weather, specific to import option.
    :param weather_input: GUI window that will be marked with incorrect input
    :return: if valid, True and dictionary {"Path": path} for weather import. Else, False and empty dict.
    """
    text = weather_input.import_path.toPlainText()
    if text == "":  # most likely valid if anything because path taken via user pointing to file
        weather_input.import_path.setStyleSheet(weather_input.error_border)  # set red border around
        return False, {}
    else:
        weather_input.import_path.setStyleSheet(weather_input.default_border)  # set back if fixed later
        return True, {"Path": text}


def gather_weather_none(weather_input):
    """
    Helper for gather_weather, specific to none option.
    :param weather_input: GUI window (unused)
    :return: True and empty dict (always valid with no parameters)
    """
    return True, {}


def gather_twilight(twilight_input):
    """
    Helper for gather_all, specific to twilight information.
    :param twilight_input: GUI window that will be marked with incorrect input
    :return: if valid, True and all information necessary to run create_rep regarding twilight. Else, False
            and empty dict.
    """
    out = {}
    need_scrape = False

    type_flag, types_options = gather_twilight_types_options(twilight_input)

    # runs even if type_flag was false because types_options always returns the status of radio buttons
    # this allows need_scrape to be flagged correctly even if types_flag will fail the program later
    out = types_options
    for twilight_type in types_options.keys():
        if types_options[twilight_type]["Action"] == "Scrape":
            need_scrape = True
            break

    if need_scrape is True:
        param_flag, common_param = gather_twilight_common_parameters(twilight_input)
        out["Parameters"] = common_param
    else:
        reset_common_parameters_border(twilight_input)

    if type_flag is False or param_flag is False:
        return False, {}
    else:
        return True, out


def gather_twilight_types_options(twilight_input):
    """
    Helper for gather_twilight, specific to twilight panel's settings for individual types (sun, moon).
    :param twilight_input: GUI window that will be marked with incorrect input
    :return: if valid, True and dictionary {type: {action: value, parameters: {...}}}. Else, False and same dict
            (for later processing purposes).
    """
    out = {}
    missing = []
    for twilight_type in twilight_input.types:
        out[twilight_type] = {}
        action = twilight_input.button_groups[twilight_type].checkedButton().text()
        out[twilight_type]["Action"] = action

        line_edit = twilight_input.abbreviated_paths[twilight_type]
        if action == "Import":
            full_path = twilight_input.full_import_paths[twilight_type].get_string()
            if full_path != "":
                out[twilight_type]["Path"] = full_path
                line_edit.setStyleSheet(twilight_input.default_border)
            else:
                missing.append(twilight_type)
                line_edit.setStyleSheet(twilight_input.error_border)
        else:
            line_edit.setStyleSheet(twilight_input.default_border)
            # need to change back if option is changed after error

    if len(missing) == 0:
        return True, out
    else:  # at least one missing input field
        first_index = twilight_input.types.index(missing[0])
        twilight_input.types_options.setCurrentIndex(first_index)
        twilight_input.combo_box.setCurrentIndex(first_index)
        # change to first missing param's window
        return False, out


def gather_twilight_common_parameters(twilight_input):
    """
    Helper for gather_twilight, specific to twilight panel's settings common parameters (City, State).
    :param twilight_input: GUI window that will be marked with incorrect input
    :return: if valid, True and dictionary {param: value}. Else, False and empty dict.
    """
    out = {}
    missing = []

    for name in twilight_input.scrape_fields.keys():
        widget = twilight_input.scrape_fields[name]
        if widget.isEnabled() is True:
            if type(widget) is QLineEdit:
                if widget.text() == "":
                    missing.append(name)
                    widget.setStyleSheet(twilight_input.error_border)
                else:
                    out[name] = widget.text()
                    widget.setStyleSheet(twilight_input.default_border)
            elif type(widget) is QCheckBox:
                out[name] = widget.isChecked()

    if len(missing) == 0:
        return True, out
    else:
        return False, {}


def reset_common_parameters_border(twilight_input):
    """
    Changes borders of all line edit fields to their default color
    :param twilight_input: GUI window that will be reset
    :return: nothing, mutates GUI
    """
    for field in twilight_input.scrape_fields.values():
        field.setStyleSheet(twilight_input.default_border)


# TODO: Finish gather_twilight, start process.py
# TODO: Translate label data gathering to the keys in backend
