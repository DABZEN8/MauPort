from flask import render_template, flash, redirect, url_for
from db import connect_db

def view_portfolio(portfolio_id):
    conn = connect_db()
    cur = conn.cursor()

    # Hämta info om portfolio
    cur.execute("""
        SELECT title, text_content 
        FROM portfolio 
        WHERE id = %s
    """, (portfolio_id,))
    portfolio = cur.fetchone()

    if not portfolio:
        flash("Portfoliot kunde inte hittas.", "danger")
        return redirect(url_for('upload_files'))

    # Hämta bilder
    cur.execute("""
        SELECT img_path 
        FROM portfolio_images 
        WHERE portfolio_id = %s
    """, (portfolio_id,))
    images = cur.fetchall()

    # Hämta videor
    cur.execute("""
        SELECT video_path 
        FROM portfolio_videos 
        WHERE portfolio_id = %s
    """, (portfolio_id,))
    videos = cur.fetchall()

    # Hämta kodfiler
    cur.execute("""
        SELECT file_path 
        FROM portfolio_code 
        WHERE portfolio_id = %s
    """, (portfolio_id,))
    codes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('portfolio.html', portfolio=portfolio, images=images, videos=videos, codes=codes)