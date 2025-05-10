from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length

# Formulär för att lagga upp filer
class UploadFileForm(FlaskForm):
    file = FileField('Välj fil', validators=[InputRequired()])
    submit = SubmitField('Ladda upp')

# Formulär för att ändra inställningar för användaren
class SettingsForm(FlaskForm):
    first_name = StringField('Förnamn', validators=[InputRequired()])
    last_name = StringField('Efternamn', validators=[InputRequired()])
    biography = TextAreaField('Biografi', validators=[Length(max=3000)])
    file = FileField('Profilbild')
    submit = SubmitField('Spara ändringar')