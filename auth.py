from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import connect_db
import psycopg2.extras
import re

def user_exists(username, email):
    """Kollar om användaren redan finns i databasen baserat på användarnamn eller e-post."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user is not None

def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        #Validera email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email.")
            return redirect('/register')
        
        #Validerar användarnamn
        elif not re.match(r"^[A-Za-z0-9_]+$", username):
            flash("Username can only contain letters, numbers and underscore.")
            return redirect('/register')
        
        #Validerar lösenord
        elif not re.match(r"^[A-Za-z0-9]+$", password):
            flash("The password can only contain letters and numbers.")

        #Kontrollera om användaren redan finns
        elif user_exists(username, email):
            flash("The username or email are already registered", "error")
            return redirect(url_for("register"))
        
        password_hash = generate_password_hash(password)

        #Lägg till användare i databas
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users(first_name, last_name, username, email, password_hash) VALUES (%s, %s, %s, %s, %s)", 
            (first_name, last_name, username, email, password_hash),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Registra!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None:
            flash('Username not found. Please try again!', 'danger')
            return render_template('login.html')
        
        if not check_password_hash(user['password_hash'], password):
            flash('Incorrect password. Please try again!', 'danger')
            return render_template('login.html')

        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html')

def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    
    response = redirect(url_for('auth.login'))
    response.cache_control.no_store = True
    return response