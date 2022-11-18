#-*- charset: utf-8 -*-
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.widgets.core import TextInput

class Form(Form):
    string_input_command = StringField("Command", [validators.Length(min=1, max=9999)])
    string_input_name = StringField("Name", [validators.Length(min=1, max=9999)])
    select_input_type = SelectField("Command Type", choices=["Raw", "HEX", "ASCII"])

