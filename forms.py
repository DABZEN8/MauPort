from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Optional, EqualTo, Regexp

password_regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
password_message = "Lösenordet måste vara minst 8 tecken och innehålla minst en versal, en siffra och ett specialtecken."

# Formulär där användare ändrar inställningar i inloggat läge
class SettingsForm(FlaskForm):
    first_name = StringField("Förnamn", validators=[DataRequired()])
    last_name = StringField("Efternamn", validators=[DataRequired()])
    username = StringField ("Användarnamn", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    program = StringField("Program")
    bio = TextAreaField("Biografi")
    submit = SubmitField("Spara ändringar")

    current_password = PasswordField("Ange ditt nuvarande lösenord", validators=[Optional()])
    new_password = PasswordField("Ange nytt lösenord", validators=[
        Optional(), 
        Regexp(password_regex, message=password_message),
        EqualTo("confirm_password", message="Lösenorden matchar inte")
    ])
    confirm_password = PasswordField("Bekräfta nytt lösenord")