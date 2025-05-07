from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

#upload = Blueprint('upload', __name__)
app = Flask('__name__')

#Denna nyckel används för att kryptera data som lagras i cookies t.ex. användarinformation mellan sidladdningar.
app.config['SECRET_KEY'] = 'temporary_secret_key'

class UploadFileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload File')

@app.route('/', methods=['GET, POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadFileForm()
    return render_template('upload.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)    
    
    