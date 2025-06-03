from flask import render_template, flash, redirect, url_for
from db import connect_db

DEFAULT_PROFILE_PIC = "profile_pictures/default_profile.jpg"

def view_portfolio(portfolio_id):
    """
    Visar ett portfolioinlägg med tillhörande media och information om ägaren.

    Funktionens syfte:
    - Hämta titel, textinnehåll och media (bilder, videor, kodfiler) för ett givet portfolioinlägg.
    - Hämta och returnera information om användaren som äger inlägget.
    - Skicka all data till portfolio.html där både inlägget och två profilkort visas.

    Parametrar:
    - portfolio_id (int): ID för portfolioinlägget som ska hämtas.

    Returnerar:
    - HTML-sida som visar inläggets innehåll, media och ägarinformation.
    """
    
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.title, p.text_content,
               u.id, u.first_name, u.last_name, u.program, u.profile_pic
        FROM portfolio p
        JOIN users u ON p.user_id = u.id
        WHERE p.id = %s
    """, (portfolio_id,))
    
    result = cur.fetchone()

    if not result:
        flash("Portfoliot kunde inte hittas.", "danger")
        return redirect(url_for('index'))

    title, text_content, user_id, first_name, last_name, program, profile_pic = result
    full_name = f"{first_name} {last_name}"
    profile_pic = profile_pic if profile_pic and profile_pic.strip() else "profile_pictures/default_profile.jpg"

    cur.execute("SELECT img_path FROM portfolio_images WHERE portfolio_id = %s", (portfolio_id,))
    images = cur.fetchall()

    cur.execute("SELECT video_path FROM portfolio_videos WHERE portfolio_id = %s", (portfolio_id,))
    videos = cur.fetchall()

    cur.execute("SELECT file_path FROM portfolio_code WHERE portfolio_id = %s", (portfolio_id,))
    codes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "portfolio.html",
        portfolio=(title, text_content),
        images=images,
        videos=videos,
        codes=codes,
        owner_id=user_id,
        owner_name=full_name,
        owner_program=program,
        owner_pic=profile_pic
    )
