from flask import Flask, render_template
from auth import register as auth_register, login as auth_login, logout as auth_logout
from upload import handle_file_upload
from settings import user_settings
from portfolio import view_portfolio
from upload import handle_file_upload
from werkzeug.utils import secure_filename
from wtforms.validators import Email
import os

app = Flask (__name__)
app.secret_key = '3d9f728e4c2b3f6f8e5a1c7a8b9d2f3e4c5a6b7d8e9f0a1b2c3d4e5f6a7b8c9d'
app.config['UPLOAD_FOLDER'] = "static"

# Route till startsidan
@app.route('/')
def index():
    return render_template("index.html")

# Route till login sidan
@app.route("/login", methods =["GET", "POST"])
def login():
    return auth_login()

@app.route("/logout")
def logout():
    return auth_logout()

@app.route("/register", methods=["GET", "POST"])
def register():
    return auth_register()

# Route till profil sidan
@app.route("/profile")
def profile():
    return render_template("profile.html")

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