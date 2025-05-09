import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from forms import UploadFileForm



upload_file = Flask(__name__)
upload_file.config['UPLOAD_FOLDER'] = 'static/files'

# Se till att uppladdningsmappen finns
upload_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_file.config['UPLOAD_FOLDER'])
os.makedirs(upload_path, exist_ok=True)


def handle_file_upload():
    form = UploadFileForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = form.file.data # Hämta filen från formuläret
        
        if file: 
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_path, filename))  # Sparar filen            
            return "Filen har laddats upp"
        else:
            return "Ingen fil har valts"
    return render_template('upload.html', form=form)