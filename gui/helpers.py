from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit, QCheckBox, QSizePolicy

from gui.exception import *


def basic_form_creator(fields, defaults=None):
    """
    General one row per field PyQT QFormLayout creator. Supports text fields and checkboxes.
    :param fields: list of lists of string name labels for each field, a string of the type of field such as:
                    "text", "checkbox"
    :param defaults: a dictionary mapping labels in fields to default entries:
                    text fields: string, checkbox: boolean
    :return: list containing initialized QFormLayout and a dictionary mapping
            string name labels to corresponding QLineEdit text fields
    """
    if defaults is None:
        defaults = {}

    out = {}
    layout = QFormLayout()

    func_map = {"text": create_textfield, "checkbox": create_checkbox}

    for field in fields:  # [name, type]
        inter = func_map[field[1].lower()](field[0], defaults)
        label, field_object = inter
        out[label] = field_object
        layout.addRow(label, field_object)

    return [layout, out]


def create_textfield(field, defaults=None):
    if defaults is None:
        defaults = {}

    label = QLabel(field)
    text = QLineEdit()

    if field in defaults.keys():
        if type(defaults[field]) is not str:
            raise FormTypeError

        text.setText(defaults[field])

    return label, text


def create_checkbox(field, defaults=None):
    if defaults is None:
        defaults = {}

    label = QLabel(field)
    checkbox = QCheckBox()

    if field in defaults.keys():
        if type(defaults[field]) is not bool:
            raise FormTypeError("create_checkbox: expected bool but got " + type(defaults[label]))

        checkbox.setChecked(defaults[field])

    return label, checkbox

