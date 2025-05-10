from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import InputRequired, DataRequired


# Formulär där användare ändrar inställningar i inloggat läge
class SettingsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    program = StringField('Program')
    bio = TextAreaField('Bio')
    profile_picture = FileField('Profile Picture')