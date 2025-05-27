from flask import render_template, session, redirect, url_for, flash
from db import connect_db

def profile():
    if "user_id" not in session:
        flash("Du måste vara inloggad för att visa din profilsida.", "danger")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT first_name, last_name, program, bio, profile_pic
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cur.fetchone()

    cur.execute("""
        SELECT id, title, thumbnail
        FROM portfolio
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    portfolios = cur.fetchall()

    cur.close()
    conn.close()

    if not user:
        flash("Kunde inte hämta användaruppgifter.", "danger")
        return redirect(url_for("login"))

    full_name = f"{user[0]} {user[1]}"
    program = user[2]
    bio = user[3]
    profile_pic = user[4]

    return render_template(
        "user_profile.html",
        full_name=full_name,
        program=program,
        bio=bio,
        profile_pic=profile_pic,
        portfolios=portfolios
    )