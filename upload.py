import os
import time
from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from db import connect_db
import psycopg2


def handle_file_upload():
    """
        Hanterar filuppladdningen via ett formulär.
        Kontrollerar att användaren är inloggad och validerarformulärdata (titel, beskrivning,thumbnail) 
        och sparar filerna lokalt samt i databasen. Om något saknas eller är fel visas ett felmeddelande 
        och användaren omdirigeras tillbaka till uppladdningssidan.
        
        Returns:
                Response: En Flask-redirect till rätt sida beroende på om uppladdningen lyckades eller inte.
        
    """
    if "user_id" not in session:
        flash("Du måste vara inloggad för att ladda upp filer!")
        return redirect(url_for("login"))

    if request.method == "POST":
        files = request.files.getlist("files")
        thumbnail_file = request.files.get("thumbnail")
        title = request.form.get("title")
        text_content = request.form.get("text_content")

        if not title:
            flash("Titel krävs.", "error")
            return redirect(url_for("upload_files"))
        
        if not text_content:
            flash("Lägg till en beskrivning!", "error")
            return redirect(url_for("upload_files"))
        
        if not thumbnail_file or thumbnail_file.filename == "":
                flash("Du måste välja en thumbnail!", "error")
                return redirect(url_for("upload_files"))

        thumbnail_filename = secure_filename(thumbnail_file.filename)
        thumbnail_path = save_file_locally(thumbnail_file, thumbnail_filename)

        if files and files[0].filename:
            portfolio_id = save_portfolio_to_database(files, title, text_content, thumbnail_path)
            return redirect(url_for("show_portfolio", portfolio_id=portfolio_id))
        else:
            flash("Ingen fil har valts")
            return redirect(url_for("upload_files"))
        
    return render_template('upload.html')


def save_portfolio_to_database(files, title, text_content, thumbnail_path):         
    """
        Sparar ett nytt portfolio-inlägg i databasen, inlusive tillhörande filer.
        Baserat på filtyp till exempel bild, video eller kod sparas filerna i olika tabeller.
        Filerna sparas först lokalt och sedan registreras deras sökvägar i databasen.
        
        Args: 
            files: list 
                  En lista med filobjekt som användaren laddat upp.
            title : str
                  Titeln på portfolion.
            text_content: str   
                    En beskrivande text för portolions innehåll.   
            thumbnail_path: str
                    Sökväg till sparad thumbnail.        

        Returns: 
                int: Unikt ID för det nya portfolio-inlägget i databasen.                
                  
    """
    
    conn = connect_db()
    cur = conn.cursor()    
            
    user_id = session.get("user_id")
         
    cur.execute("""
        INSERT INTO portfolio (user_id, title, text_content, thumbnail)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (user_id, title, text_content, thumbnail_path))

    portfolio_id = cur.fetchone()[0]

    for file in files: 
        filename = secure_filename(file.filename)  
        relative_path = save_file_locally(file, filename)
        file_extension = filename.lower().split('.') [-1]  
        file_content = file.read() 
          
        if file_extension in ["jpg" , "jpeg", "png"]: 
            cur.execute ("""
                         INSERT INTO portfolio_images (portfolio_id, img_path)
                         VALUES( %s, %s)
                    """, (portfolio_id, relative_path)) 
            
        elif  file_extension in ["mp4", "mov"]:
            cur.execute(""" 
                        INSERT INTO portfolio_videos (portfolio_id, video_path)
                        VALUES (%s, %s) 
                    """, (portfolio_id, relative_path))     
        
        elif file_extension in ["py", "txt"]:
            cur.execute("""
                        INSERT INTO portfolio_code (portfolio_id, file_path)
                        VALUES (%s, %s)
                    """, (portfolio_id, psycopg2.Binary(file_content)))

        else:
            print("Denna filtyp stöds inte", file_extension)

    conn.commit()
    cur.close()
    conn.close()
    return portfolio_id
                
def save_file_locally(file, filename):
    """ Sparar en uppladdad fil lokalt i mappen 'static/project_uploads'. 
        Om en fil med samma namn redan existerar läggs en tidstämpel till i början av filnmanet
        för att undvika överskrivning. 
        
        Args: 
            file: FileStorage
                    Filobjektet som ska sparas exempelvis från en Flask-formulärupload).
            filename: str
                    Det önskade filnamnet inklusive filändelse.
        
        Returns: 
            str: Den relativa sökvägen till den sparade filen, avsedd för lagring i databasen. 
    """
    from app import app

    upload_folder = os.path.join(app.root_path, "static", "project_uploads")
    os.makedirs(upload_folder, exist_ok=True)

    # Skapa en första file_path
    file_path = os.path.join(upload_folder, filename)
    
    # Kontrollera om filen redan finns
    if os.path.exists(file_path):
        filename = f"{int(time.time())}_{filename}"  # Lägg till timestamp för unikt namn
        file_path = os.path.join(upload_folder, filename)  # Uppdatera path med nya filnamnet

    # Spara filen
    file.save(file_path)

    # Returnera relativ sökväg (till databasen)
    return os.path.join("project_uploads", filename).replace("\\", "/")
