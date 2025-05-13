from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# Formulär där användare ändrar inställningar i inloggat läge
class SettingsForm(FlaskForm):
    first_name = StringField("Förnamn", validators=[DataRequired()])
    last_name = StringField("Efternamn", validators=[DataRequired()])
    username = StringField ("Användarnamn", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    program = StringField("Program")
    bio = TextAreaField("Biografi")
    submit = SubmitField("Spara ändringar")