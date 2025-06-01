from flask import render_template, session, redirect, url_for, flash
from db import connect_db

def profile(user_id=None):
    """Visar användarens egen profil eller en annan användares profil baserat på user_id."""
    viewing_own = False
    if user_id is None:
        if "user_id" not in session:
            flash("Du måste vara inloggad för att visa din profilsida.", "danger")
            return redirect(url_for("login"))
        user_id = session["user_id"]
        viewing_own = True
    elif "user_id" in session and session["user_id"] == user_id:
        viewing_own = True

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT first_name, last_name, username, program, email, bio, profile_pic
        FROM users
        WHERE id = %s
    """, (user_id,))
    user = cur.fetchone()

    if not user:
        flash("Användaren kunde inte hittas.", "danger")
        return redirect(url_for("index"))

    cur.execute("""
        SELECT id, title, thumbnail
        FROM portfolio
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    portfolios = cur.fetchall()

    cur.close()
    conn.close()

    full_name = f"{user[0]} {user[1]}"
    return render_template(
        "profile.html",
        full_name=full_name,
        username=user[2],
        program=user[3],
        email=user[4],
        bio=user[5],
        profile_pic=user[6] or "profile_pictures/default_profile.jpg",
        portfolios=portfolios,
        is_own_profile=viewing_own
    )
