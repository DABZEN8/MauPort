import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from db import connect_db
import psycopg2


upload_file = Flask(__name__)

# Hanterar filuppladdningen
def handle_file_upload():
    
    if request.method == 'POST':
        #file = form.file.data # Hämta filen från formuläret
        files = request.files.getlist("file")
        
        if files and files[0].filename!='':
            portfolio_id = save_portfolio_to_database(files)           
            return f"Filen har laddats upp i din portfolio {portfolio_id}"
        else:
            return "Ingen fil har valts"
    return render_template('upload.html')




    
    
    