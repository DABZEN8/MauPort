import os
import time
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from db import connect_db
import psycopg2



# Hanterar filuppladdningen
def handle_file_upload():

    if request.method == 'POST':
        #file = form.file.data # Hämta filen från formuläret
        files = request.files.getlist("file")

        if files and files[0].filename:
            portfolio_id = save_portfolio_to_database(files)
            return f"Filen har laddats upp i din portfolio {portfolio_id}"
        else:
            return "Ingen fil har valts"
    return render_template('upload.html')


#sparar filerna i databasen
def save_portfolio_to_database(files):
                
    conn = connect_db()
    cur = conn.cursor()    
            
    user_id = 1
    title = "Exempel"
    description = "Uppladdad fil"
    text_content = ""
                
    
    cur.execute("""
        INSERT INTO portfolio (user_id, title, description, text_content)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """, (user_id, title, description, text_content))

    save_file_locally(files, portfolio_id)           
    portfolio_id = cur.fetchone()[0]


    for file in files: 
        filename = secure_filename(file.filename)  
        relative_path = save_file_locally(file, filename)
        file_extension = filename.lower().split('.') [-1]   
        file_content = file.read()
          

        if file_extension in ['jpg' , 'jpeg', 'png']: 
            cur.execute (""" INSERT INTO port.img (portf_id, img_path))
                         VALUES( %s, %s) """, 
                         (portfolio_id, relative_path)) 
        
        elif  file_extension in ['mp4', 'mov']:
               cur.execute(""" 
                           INSERT INTO port.video (portf_id, video_path)
                           VALUES (%s, %s) """,
                           (portfolio_id, relative_path))     
        
        elif file_extension in ['py', 'txt']: 
            cur.execute(""" 
                        INSERT INTO code.projekt (portf_id, file_link)
                        VALUES (%s, %s)""", 
                        (portfolio_id, psycopg2.Binary(file_content)))   
            
        else:
            print("Denna filtyp stöds inte", file_extension)



    conn.commit()
    cur.close()
    conn.close()
    return portfolio_id
                
    
 #Sparar filen fysiskt på servern och returnerar relativ sökväg till databasen.
def save_file_locally(file, filename):
    from app import app
    upload_folder = app.config['UPLOAD_FOLDER']

    # Se till att uppladdningsmappen finns
    upload_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), upload_folder)
    
    os.makedirs(upload_path, exist_ok=True)

    file_path = os.path.join(upload_path,filename)
    
     # Kontrollera om filen redan finns
    if os.path.exists(file_path):
       filename = f'{int(time.time())}_{filename}' #Detta är en tidsstämpel som säkerställer att filer man samma namn inte skrivs över.
       file_path = os.path.join(upload_path, filename)

    with open(file_path , 'wb') as upload_portfolio:
        upload_portfolio.write(file.read()) 

    return os.path.join(upload_folder, filename)

    
    