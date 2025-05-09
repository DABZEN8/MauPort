import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from forms import UploadFileForm
from db import connect_db
import psycopg2


upload_file = Flask(__name__)

# Hanterar filuppladdningen
def handle_file_upload():
    
    form = UploadFileForm()
    if request.method == 'POST' and form.validate_on_submit():
        #file = form.file.data # Hämta filen från formuläret
        files = request.files.getlist("file")
        
        if files:
            save_portfolio_to_database(files)           
            return "Filen har laddats upp"
        else:
            return "Ingen fil har valts"
    return render_template('upload.html', form=form)

#sparar filerna i databasen
def save_portfolio_to_database(files):
                
    user_id = 1
    title = "Exempel"
    description = "Uppladdad fil"
    text_content = ""
    image_path = None
    video_path = None

                
    conn = connect_db()
    cur = conn.cursor()
                
    cur.execute("""
        INSERT INTO portfolio (
        user_id, title, description, text_content, image_path, video_path, code_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, title, description, text_content,None, None, psycopg2.Binary(file_content)))
                
    # cur.execute(insert_query, (
    # user_id, title, description, text_content,
    # image_path, video_path, psycopg2.Binary(file_content)))
    save_file_locally(files, portfolio_id)           
                
    conn.commit()
    cur.close()
    conn.close()

    

def save_file_locally(files, portfolio_id):
    upload_file.config['UPLOAD_FOLDER'] = 'files/portfolio_files'

    # Se till att uppladdningsmappen finns
    upload_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_file.config['UPLOAD_FOLDER'])
    
    os.makedirs(upload_path, exist_ok=True)
    
    image_path = os.path.join(upload_path,filename)
    
    with open(image_path , 'wb') as image:
        image.write(file.read()) 

    return image_path
    
    