import os
import time
import re
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db import connect_db
from forms import SettingsForm

# Tillåtna filformat för profilbilder
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Kontrollerar att filändelsen är korrekt
def allowed_file(filename):
    """
    Kontrollerar om en fil har en tillåten filändelse (profilbild).
    
    Parametrar:
    - filename (str): namnet på den fil som ska kontrolleras.
    
    Returnerar:
    - bool: True om filändelsen är tillåten (.png, .jpg, .jpeg), annars False.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Visa/ändra användarens inställningar
def user_settings():
    """
    Visar och behandlar formuläret för att ändra användarens kontoinställningar.
    
    Syfte:
    - Ladda användarens aktuella info i formuläret vid GET-förfrågan.
    - Validera och uppdatera informationen vid POST-förfrågan.
    - Hantera profilbilds- och lösenordsändring.
    - Säkerställa att endast inloggade användare kan ändra sina inställningar.
    
    Returnerar:
    - HTML-sida "settings.html" med formuläret och aktuell profilbild.
    - Redirect till login om användaren inte är inloggad.
    - Redirect till inställningssidan med flashmeddelanden efter ändringar.
    """
    form = SettingsForm()
    current_profile_picture = None

    # Session för att kontrollera att en användare är inloggad
    if "user_id" not in session:
        flash("Du måste vara inloggad för att ändra inställningar.", "danger")
        return redirect(url_for("login"))

    # Databasanslutning
    conn = connect_db()
    cursor = conn.cursor()

    # Kontrollerar hur formuläret skickas och att det är korrekt ifyllt
    if request.method == "POST" and form.validate_on_submit():

        # Ta emot fälten från användaren
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        bio = form.bio.data
        program = form.program.data
        new_password = form.new_password.data

        # Hantera profilbildens sökväg
        new_profile_picture_path = None
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file and file.filename != "" and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # Spara i /static/profile_pictures/
                upload_folder = os.path.join("static", "profile_pictures")
                os.makedirs(upload_folder, exist_ok=True)

                file_path = os.path.join(upload_folder, filename)

                # Lägger till timestamp för att inte skriva över eventuella filer med samma namn från annan användare
                if os.path.exists(file_path):
                    filename = f"{int(time.time())}_{filename}"
                    file_path = os.path.join(upload_folder, filename)

                # Sparar filen på servern
                file.save(file_path)

                # Relativ sökväg som sparas i databasen
                new_profile_picture_path = os.path.join("profile_pictures", filename)

        # Om ingen ny bild laddas upp, använd nuvarande
        if not new_profile_picture_path:
            new_profile_picture_path = current_profile_picture or "profile_pictures/default_profile.jpg"

        try:
            current_password = form.current_password.data
            new_password = form.new_password.data

            if new_password:
                cursor.execute("SELECT password_hash FROM users WHERE id = %s", (session["user_id"],))
                db_password_hash = cursor.fetchone()[0]

                if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", new_password):
                    flash("Lösenordet måste innehålla minst 8 tecken och inkludera en versal, en siffra och ett specialtecken.", "danger")
                    return redirect(url_for("settings"))

                if not check_password_hash(db_password_hash, current_password):
                    flash("Nuvarande lösenord är felaktigt", "danger")
                    return redirect(url_for("settings"))
                

                password_hash = generate_password_hash(new_password)

                # Uppdaterar användarens information i databasen
                cursor.execute("""
                    UPDATE users
                    SET first_name = %s,
                        last_name = %s,
                        username = %s,
                        email = %s,
                        bio = %s,
                        program = %s,
                        profile_pic = %s,
                        password_hash = %s
                    WHERE id = %s
                """, (first_name, last_name, username, email, bio, program, new_profile_picture_path, password_hash, session['user_id']))

            else:
                cursor.execute("""
                    UPDATE users
                    SET first_name = %s,
                        last_name = %s,
                        username = %s,
                        email = %s,
                        bio = %s,
                        program = %s,
                        profile_pic = %s
                    WHERE id = %s
                """, (first_name, last_name, username, email, bio, program, new_profile_picture_path, session['user_id']))

            conn.commit()
            flash("Dina ändringar har sparats!", "success")
            return redirect(url_for('settings'))

        except Exception as e:
            conn.rollback()
            flash(f"Fel vid sparning: {e}", "danger")

    else:
        # GET: Läs nuvarande användardata
        cursor.execute("""
            SELECT first_name, last_name, username, email, bio, program, profile_pic
            FROM users
            WHERE id = %s
        """, (session["user_id"],))
        user = cursor.fetchone()

        if user:
            form.first_name.data = user[0]
            form.last_name.data = user[1]
            form.username.data = user[2]
            form.email.data = user[3]
            form.bio.data = user[4]
            form.program.data = user[5]
            current_profile_picture = user[6]

    # Stäng anslutningen till databasen
    cursor.close()
    conn.close()

    # Visa inställningssidan och skicka formulär/profilbild
    return render_template("settings.html", form=form, profile_picture=current_profile_picture)