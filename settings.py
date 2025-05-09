# settings.py

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
    # Session då ändringar enbart ska ske i inloggat läge
    if 'user_id' not in session:
        flash("Logga in för att se och ändra dina inställningar.")
        return redirect(url_for('login'))

    user_id = session['user_id']
    form = SettingsForm() # Formulär för inställningar i forms.py

    # Validerar att uppgifterna är korrekt ifyllda
    if request.method == 'POST' and form.validate_on_submit():
        file = form.file.data
        profile_pic = None

        # Profilbild
        if file:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('static/profile_pics')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            profile_pic = filename

        # Anslut till och uppdatera användaren i databasen        
        conn = connect_db()
        cursor = conn.cursor()
        if profile_pic:
            cursor.execute("""
                UPDATE users
                SET first_name = %s, last_name = %s, bio = %s, profile_pic = %s
                WHERE id = %s
            """, (form.first_name.data, form.last_name.data, form.biography.data, profile_pic, user_id))
        else:
            cursor.execute("""
                UPDATE users
                SET first_name = %s, last_name = %s, bio = %s
                WHERE id = %s
            """, (form.first_name.data, form.last_name.data, form.biography.data, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Inställningarna har uppdaterats!", "success")
        return redirect(url_for('settings')) # Laddar om sidan

    # Hämtar användarens aktuella data från databasen
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, bio FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        form.first_name.data = user[0]
        form.last_name.data = user[1]
        form.biography.data = user[2]

    # Skickar formuläret till HTML-sidan
    return render_template('settings.html', form=form)