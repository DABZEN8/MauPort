from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


# Formulär där användare ändrar inställningar i inloggat läge
class SettingsForm(FlaskForm):
    first_name = StringField("Förnamn", validators=[DataRequired()])
    last_name = StringField("Efternamn", validators=[DataRequired()])
    username = StringField ("Användarnamn", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    program = StringField("Program")
    biography = StringField("Biografi")
    submit = SubmitField("Spara ändringar")