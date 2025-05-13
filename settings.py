from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from forms import SettingsForm
from db import connect_db
import os

def user_settings():
    """Kontrollerar:
    - Om användaren är inloggad.
    - Uppdaterar/hämtar användaren i/från databasen
    """
    form = SettingsForm()

    # Session då ändringar enbart ska ske i inloggat läge
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()

    # Validerar att uppgifterna är korrekt ifyllda
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        program = form.program.data
        biography = form.bio.data

        profile_picture_path = None

        # Profilbild där fil är bifogad
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                upload_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "profile_pics")
                os.makedirs(upload_folder, exist_ok=True)
            
                file_path = os.path.join(upload_folder, filename)

        try: 
            if profile_picture_path:
                cursor.execute("""
                    UPDATE users
                    SET first_name = %s, 
                        last_name = %s, 
                        username = %s, 
                        email = %s,
                        program = %s,
                        biography = %s,
                        profile_picture = %s
                    WHERE id = %s
                """, (first_name, last_name, username, email, program, biography, profile_picture_path, session["user_id"]))
            else:
                cursor.execute("""
                    UPDATE users
                    SET first_name = %s, 
                        last_name = %s, 
                        username = %s, 
                        email = %s,
                        program = %s,
                        biography = %s,
                        profile_picture = %s
                    WHERE id = %s
                """, (first_name, last_name, username, email, program, biography, profile_picture_path, session["user_id"]))
            
            conn.commit()
            flash("Ändringar sparade!", "success")
            return redirect(url_for("settings"))
    
        except Exception as e:
            conn.rollback()
            flash("Ett fel uppstod när ändringarna skulle sparas")

        else:
            cursor.execute("""
                SELECT first_name, last_name, username, email, program, biography
                FROM users
                WHERE id = %s
            """, (session["user_id"],))
            user = cursor.fetchone()

            if user:
                form.first_name.data = user [0]
                form.last.data = user [1]
                form.username.data = user [2]
                form.email.data = user [3]
                form.program.data = user [4]
                form.biography.data = user [5]

            else: 
                flash("Användaren hittades ej")
                return redirect(url_for("login"))


        cursor.close()
        conn.close()
        
    # Skickar formuläret till HTML-sidan
    return render_template('settings.html', form=form)