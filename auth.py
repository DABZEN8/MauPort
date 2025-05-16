from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import connect_db
import psycopg2.extras
import re

def user_exists(username, email):
    """Kollar om användaren redan finns i databasen baserat på användarnamn eller e-post."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        user = cursor.fetchone()
        return user is not None
    
    except psycopg2.Error as e:
        flash(f"Database error: {str(e)}", "error")
        return None
    
    finally:
        if 'cursor' in locals(): # Stängs bara om 'cursor' finns
            cursor.close()
        if 'conn' in locals(): # Stängs bara om 'conn' finns
            conn.close()

def register():
    if request.method == 'POST':
        form_data = request.form.copy()  # Gör en kopia med alla inputs
        form_data.pop('password', None)  # Ta bort lösenord från form_data

        first_name = form_data.get('first_name').capitalize()
        last_name = form_data.get('last_name').capitalize()
        username = form_data.get('username')
        username = username.capitalize() if username else username
        email = form_data.get('email')

        # Validera namn och efternamn
        if not re.match(r"^[A-Za-z]+$", first_name) or not re.match(r"^[A-Za-z]+$", last_name):
            flash("För- och efternamn kan endast innehålla bokstäver.")
            return render_template('register.html', form_data=form_data)

        # Validerar användarnamn
        if not re.match(r"^(?=.*[A-Za-z])[A-Za-z0-9_]+$", username):
            flash("Användarnamn kan endast innehålla bokstäver, siffror och understreck.")
            return render_template('register.html', form_data=form_data)

        # Validera email
        if not re.match(r"^[A-Za-z0-9._%+-]+@(hotmail|gmail|outlook|yahoo)\.com$", email):
            flash("Ogiltig email.")
            return render_template('register.html', form_data=request.form)
        
        # Validerar lösenord
        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
            flash("Lösenordet måste innehålla minst 8 karaktärer och inkludera en versal, en siffra och ett specialtecken.")
            return render_template('register.html', form_data=form_data)

        password = request.form['password']

        # Kontrollera om användaren redan finns
        if user_exists(username, email):
            flash("Användarnamn eller email finns redan registrerat.", "error")
            return render_template('register.html', form_data=form_data)

        password_hash = generate_password_hash(password)

        # Lägg till användare i databas
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users(first_name, last_name, username, email, password_hash) VALUES (%s, %s, %s, %s, %s)", 
                (first_name, last_name, username, email, password_hash)
            )
            conn.commit()
            flash("Registrering lyckades!", "success")
            return redirect(url_for('login'))
        
        except psycopg2.Error as e:
            flash(f"Database error: {str(e)}", "error")
            return render_template('register.html', form_data=form_data)

        finally:
            if 'cursor' in locals() and not cursor.closed:
                cursor.close()
            if 'conn' in locals() and not conn.closed:
                conn.close()

    return render_template('register.html', form_data={})

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = None

        try:
            conn = connect_db()
            if not conn:
                flash("Could not connect to the database.", "error")
                return redirect(url_for('login'))
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

        except psycopg2.Error as e:
            flash(f"Database error: {str(e)}", "error")

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals()and conn:
                conn.close()

        if user is None:
            flash("Felaktiga uppgifter. Försök igen.", "danger")
            return redirect(url_for('login'))
        
        if not check_password_hash(user['password_hash'], password):
            flash("Felaktiga uppgifter. Försök igen!", "danger")
            return redirect(url_for('login'))

        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('Login successful!', 'success')
        redirect(url_for('index'))
    
    return render_template('login.html')

def logout():
    session.clear()
    flash("Du har loggats ut.", "info")
    
    response = redirect(url_for('login'))
    response.cache_control.no_store = True
    return response