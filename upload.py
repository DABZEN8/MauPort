import os
import time
from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from db import connect_db
import psycopg2



# Hanterar filuppladdningen
def handle_file_upload():
    if "user_id" not in session:
        flash("Du måste vara inloggad för att ladda upp filer!")
        return redirect(url_for("login"))

    if request.method == 'POST':
        files = request.files.getlist("file")
        title = request.form.get("title")
        text_content = request.form.get("text_content")
        thumbnail = request.form.get("thumbnail")

        if files and files[0].filename:
            portfolio_id = save_portfolio_to_database(files, title, text_content, thumbnail)
            return redirect(url_for("show_portfolio", portfolio_id=portfolio_id))
        else:
            flash("Ingen fil har valts")
            return redirect(url_for("upload_files"))
        
    return render_template('upload.html')

# Sparar filerna i databasen
def save_portfolio_to_database(files, title, text_content, thumbnail):         
    conn = connect_db()
    cur = conn.cursor()    
            
    user_id = session.get("user_id")

    if not title:
        title = "Titel saknas"
    if not text_content:
        text_content = "Beskrivning saknas"
    if not thumbnail:
        thumbnail = "Okategoriserad"
                
    cur.execute("""
        INSERT INTO portfolio (user_id, title, text_content, thumbnail)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (user_id, title, text_content, thumbnail))

    portfolio_id = cur.fetchone()[0]

    for file in files: 
        filename = secure_filename(file.filename)  
        relative_path = save_file_locally(file, filename)
        file_extension = filename.lower().split('.') [-1]  
        file_content = file.read() 
          
        if file_extension in ['jpg' , 'jpeg', 'png']: 
            cur.execute ("""INSERT INTO portfolio_images (portfolio_id, img_path)
                         VALUES( %s, %s)""", 
                         (portfolio_id, relative_path)) 
            
        elif  file_extension in ['mp4', 'mov']:
            cur.execute(""" 
                        INSERT INTO portfolio_videos (portfolio_id, video_path)
                        VALUES (%s, %s) """,
                        (portfolio_id, relative_path))     
        
        elif file_extension in ['py', 'txt']: 
            cur.execute(""" 
                        INSERT INTO portfolio_code (portfolio_id, file_path)
                        VALUES (%s, %s)""", 
                        (portfolio_id, psycopg2.Binary(file_content)))   
        else:
            print("Denna filtyp stöds inte", file_extension)

    conn.commit()
    cur.close()
    conn.close()
    return portfolio_id
                
 # Sparar filen fysiskt på servern och returnerar relativ sökväg till databasen.
def save_file_locally(file, filename):
    from app import app

    upload_folder = os.path.join(app.root_path, "static", "project_uploads")
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    
     # Kontrollera om filen redan finns
    if os.path.exists(file_path):
       filename = f'{int(time.time())}_{filename}' # Detta är en tidsstämpel som säkerställer att filer man samma namn inte skrivs över.
       file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    return os.path.join("project_uploads", filename)