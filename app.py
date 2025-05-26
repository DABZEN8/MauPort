"""
MauPorts huvudfil för Flask applikationen.

Denna fil gör följande:
- Registrerar alla routes för webbsidor
- Kopplar moduler som hanterar inloggning, uppladdning och visning
- Definierar grundinställningar för appen

"""
from flask import Flask, render_template
from auth import register as auth_register, login as auth_login, logout as auth_logout
from upload import handle_file_upload
from settings import user_settings
from portfolio import view_portfolio
from upload import handle_file_upload
from user_profile import profile as user_profile_view
from werkzeug.utils import secure_filename
from wtforms.validators import Email
from db import connect_db
import os

app = Flask (__name__)


app.secret_key = '3d9f728e4c2b3f6f8e5a1c7a8b9d2f3e4c5a6b7d8e9f0a1b2c3d4e5f6a7b8c9d'

#Här sparas alla uppladdade filer
app.config['UPLOAD_FOLDER'] = "static"

# Route till startsidan - listar alla portfolioinlägg
@app.route('/')
def index():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.id, p.title, p.description, p.thumbnail, p.created_at, u.username, img.img_path
        FROM portfolio p
        JOIN users u ON p.user_id = u.id
        LEFT JOIN portfolio_images img ON p.id = img.portfolio_id
        ORDER BY p.created_at DESC
    """)
    portfolios = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", portfolios=portfolios)


# Route till login sidan
@app.route("/login", methods =["GET", "POST"])
def login():
    return auth_login()

# Utloggning som avslutar inloggningsessionen
@app.route("/logout")
def logout():
    return auth_logout()

# Route till registreringssidan
@app.route("/register", methods=["GET", "POST"])
def register():
    return auth_register()

# Route till profil sidan
@app.route("/profile")
def profile():
    return user_profile_view()

# Route till portfoliosidan
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

# Route till sida för att ladda upp inlägg
@app.route("/upload", methods=["GET", "POST"])
def upload_files():
    return handle_file_upload()

# Route till sida för inställningar
@app.route("/settings", methods=["GET", "POST"])
def settings():
    return user_settings()

@app.route("/about")
def om_oss():
    return render_template("about.html")


# Route till enskilt portfolio
@app.route('/portfolio/<int:portfolio_id>')
def show_portfolio(portfolio_id):
    return view_portfolio(portfolio_id)

# Route till felhantering 
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# Säkerställer att fel meddelas under testning
if __name__ == "__main__":
    app.run(debug=True)