# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashReactDatepicker(Component):
    """A DashReactDatepicker component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- selected (string; optional): Selected date. Updates when a new date or time is selected in the datepicker.
Accepts and returns strings in ISO 8601 format.
- dateFormat (string; default 'dd.MM.yyyy'): Format to display date and time when selected.
- placeholderText (string; optional): Placeholder text to display before a value is selected.
- showTimeSelect (boolean; default False): Whether to show time selection.
- showTimeSelectOnly (boolean; default False): Whether to only show time selection. Should only be used with showTimeSelect=True.
- timeFormat (string; default 'HH:mm'): Format to display times in the picker.
- timeIntervals (number; default 30): Intervals of time to display in the picker. Should only be used with showTimeSelect=True.
- timeCaption (string; default 'Time'): Caption for the time picker."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, selected=Component.UNDEFINED, dateFormat=Component.UNDEFINED, placeholderText=Component.UNDEFINED, showTimeSelect=Component.UNDEFINED, showTimeSelectOnly=Component.UNDEFINED, timeFormat=Component.UNDEFINED, timeIntervals=Component.UNDEFINED, timeCaption=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'selected', 'dateFormat', 'placeholderText', 'showTimeSelect', 'showTimeSelectOnly', 'timeFormat', 'timeIntervals', 'timeCaption']
        self._type = 'DashReactDatepicker'
        self._namespace = 'dash_react_datepicker'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'selected', 'dateFormat', 'placeholderText', 'showTimeSelect', 'showTimeSelectOnly', 'timeFormat', 'timeIntervals', 'timeCaption']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashReactDatepicker, self).__init__(**args)
