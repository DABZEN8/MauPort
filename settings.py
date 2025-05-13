from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from db import connect_db
from forms import SettingsForm
import os
import time

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "-" in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def user_settings():
    """Kontrollerar:
    - Om användaren är inloggad.
    - Uppdaterar/hämtar användaren i/från databasen
    """
    form = SettingsForm()
    current_profile_picture = None

    # Session då ändringar enbart ska ske i inloggat läge
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = connect_db()
    cursor = conn.cursor()

    # Validerar att uppgifterna är korrekt ifyllda
    if request.method == 'POST' and form.validate_on_submit():

        # Värden från formuläret i inställningar
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        program = form.program.data
        bio = form.bio.data

        new_profile_picture_path = None

        # Profilbild där fil är bifogad
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file and file.filename != "" and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                upload_folder = os.path.join("static", "files", "portfolio_files")
                os.makedirs(upload_folder, exist_ok=True)
            
                file_path = os.path.join(upload_folder, filename)

                if os.path.exists(file_path):
                    filename = f"{int(time.time())}_{filename}"
                    file_path = os.path.join(upload_folder, filename)

                    file.save(file_path)

                    new_profile_picture_path = os.path.join("files", "portfolio_files", filename)

        if not new_profile_picture_path:
            new_profile_picture_path = current_profile_picture

        try: 
            if new_profile_picture_path:
                cursor.execute("""
                    UPDATE users
                    SET first_name = %s, 
                        last_name = %s, 
                        username = %s, 
                        email = %s,
                        program = %s,
                        bio = %s,
                        profile_pic = %s
                    WHERE id = %s
                """, (first_name, last_name, username, email, program, bio, new_profile_picture_path, session["user_id"]))

            else:
                cursor.execute("""
                    UPDATE users
                    SET first_name = %s, 
                        last_name = %s, 
                        username = %s, 
                        email = %s,
                        program = %s,
                        bio = %s
                    WHERE id = %s
                """, (first_name, last_name, username, email, program, bio, session["user_id"]))
            
            conn.commit()
            flash("Ändringar sparade!", "success")
            return redirect(url_for("settings"))
    
        except Exception as e:
            conn.rollback()
            flash("Ett fel uppstod när ändringarna skulle sparas")
            print(f"DEBUG: SQL-Fel: {e}")

    try:
        cursor.execute("""
            SELECT first_name, last_name, username, email, program, bio, profile_pic
            FROM users
            WHERE id = %s
        """, (session["user_id"],))
        user = cursor.fetchone()

        if user:
            form.first_name.data = user [0]
            form.last_name.data = user [1]
            form.username.data = user [2]
            form.email.data = user [3]
            form.program.data = user [4]
            form.bio.data = user [5]
            current_profile_picture = user [6]


        else: 
            flash("Användaren hittades ej")
            return redirect(url_for("login"))
            
    except Exception as e:
        flash(f"Fel vid hämtning av användardata")

    finally:
        cursor.close()
        conn.close()

    # Skickar formuläret till HTML-sidan
    return render_template('settings.html', form=form, profile_picture=current_profile_picture)