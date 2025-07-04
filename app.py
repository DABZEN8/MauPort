"""
MauPorts huvudfil för Flask applikationen.

Denna fil gör följande:
- Registrerar alla routes för webbsidor
- Kopplar moduler som hanterar inloggning, uppladdning och visning
- Definierar grundinställningar för appen

"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash  
from auth import register as auth_register, login as auth_login, logout as auth_logout
from upload import handle_file_upload
from settings import user_settings
from portfolio import view_portfolio
from upload import handle_file_upload
from search_results import search_portfolios
from user_profile import profile as user_profile_view
from werkzeug.utils import secure_filename #Ska denna plockas bort? Används ej i nuläget.
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
    """
    Denna funktion visar startsidan med alla portfolioinlägg.

    Hämtar en lista över alla uppladdade portfolios från databasen, 
    tillsammans med användarnamn och annan info. Om en användare är inloggad 
    kollas även vilka inlägg hen har sparat som favoriter. All data skickas 
    sedan vidare till index.html för visning.
    """
        
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
        p.id, p.title, p.description, p.thumbnail, p.created_at, u.username
        FROM portfolio p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.id DESC
    """)

    portfolios = cur.fetchall()

    saved_ids = []
    if "user_id" in session:
        cur.execute("SELECT portfolio_id FROM saved_portfolios WHERE user_id = %s", (session["user_id"],))
        saved_rows = cur.fetchall()
        saved_ids = [row[0] for row in saved_rows]

    cur.close()
    conn.close()

    return render_template("index.html", portfolios=portfolios, saved_ids=saved_ids)



# Route till login sidan
@app.route("/login", methods =["GET", "POST"])
def login():
    """
    Visar inloggningssidan och hanterar inloggning.

    Vid GET visas formuläret, vid POST behandlas inloggningen via auth_login().
    """
    return auth_login()

# Utloggning som avslutar inloggningsessionen
@app.route("/logout")
def logout():
    """
    Loggar ut användaren och avslutar sessionen.

    Skickar användaren vidare till startsidan efter utloggning.
    """
    return auth_logout()

# Route till registreringssidan
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Visar registreringssidan och hanterar skapande av konto.

    Vid GET visas formuläret, vid POST behandlas registreringen via auth_register().
    """
    return auth_register()

# Route till profil sidan
@app.route("/profile")
def profile():
    return user_profile_view()

@app.route("/profile/<int:user_id>")
def view_user_profile(user_id):
    return user_profile_view(user_id=user_id)  # andras profil

# Route till portfoliosidan
@app.route("/portfolio")
def portfolio():
    """
    Returnerar portfoliosidan och dess innehåll.
    """

    return render_template("portfolio.html")

# Route till sida för att ladda upp inlägg
@app.route("/upload", methods=["GET", "POST"])
def upload_files():
    """
    Hanterar HTTP-förfrågningar för att ladda upp filer till servern.

    GET:
        Returnerar en sida eller ett svar som tillåter användaren att ladda upp filer.

    POST:
        Tar emot uppladdade filer från användaren och bearbetar dem via funktionen
        handle_file_upload
    """
    return handle_file_upload()

# Route till sida för inställningar
@app.route("/settings", methods=["GET", "POST"])
def settings():
    return user_settings()

@app.route("/about")
def om_oss():
    """
    Returnerar Om oss-sidan och dess innehåll.
    """
    return render_template("about.html")

# Route till enskilt portfolio
@app.route('/portfolio/<int:portfolio_id>')
def show_portfolio(portfolio_id):
    """
    Returnerar korrekt portfoliosida som användaren klickar på.
    """
    return view_portfolio(portfolio_id)

# Route till felhantering 
@app.errorhandler(404)
def page_not_found(e):
    """
    Felhantering: Returnerar sida på ett felmeddelande till användare.
    """
    return render_template("404.html")

#Route till sökfunktion
@app.route("/search")
def search():
    """
    Hanterar sökförfrågningar för portföljer.
    Den tar emot sökparametrar från användaren och returnerar relevanta portföljer 
    baserat på sökningar.

    Returns:
            Response: Ett HTTP-svar som innehåller sökresultaten för portföljer.
    """

    return search_portfolios()

from flask import request, jsonify

# Route för att spara inlägg
@app.route("/save_favorite", methods=["POST"])
def save_favorite():
    """
    Sparar ett portfolioinlägg som favorit för den inloggade användaren.

    Lägger till en rad i tabellen saved_portfolios om inlägget inte redan är sparat.
    Returnerar ett JSON-svar som bekräftar om operationen lyckades eller misslyckades.
    """

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Du måste vara inloggad för att spara favoriter."}), 403

    data = request.get_json()
    portfolio_id = data.get("portfolio_id")
    user_id = session["user_id"]

    if not portfolio_id:
        return jsonify({"success": False, "message": "Portfolio saknas."}), 400

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO saved_portfolios (user_id, portfolio_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, portfolio_id) DO NOTHING
        """, (user_id, portfolio_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/favorites")
def favorites():
    """
    Visar användarens sparade portfolioinlägg.

    Om användaren inte är inloggad skickas hen till inloggningssidan.
    Hämtar användarens info och en lista på inlägg som markerats som favoriter.
    Allt skickas till favorites.html för att visas tillsammans med profilinformation.
    """

    if "user_id" not in session:
        flash("Logga in för att se dina favoriter.", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = connect_db()
    cur = conn.cursor()

    # Hämta användarens information
    cur.execute("""
        SELECT first_name, last_name, username, program, email, bio, profile_pic
        FROM users
        WHERE id = %s
    """, (user_id,))
    user = cur.fetchone()

    # Hämta sparade portfolios
    cur.execute("""
        SELECT p.id, p.title, p.thumbnail, u.username
        FROM saved_portfolios sp
        JOIN portfolio p ON sp.portfolio_id = p.id
        JOIN users u ON p.user_id = u.id
        WHERE sp.user_id = %s
        ORDER BY sp.created_at DESC
    """, (user_id,))
    favorites = cur.fetchall()

    cur.close()
    conn.close()

    full_name = f"{user[0]} {user[1]}"
    profile_pic = user[6] or "profile_pictures/default_profile.jpg"

    return render_template("favorites.html",
        favorites=favorites,
        full_name=full_name,
        username=user[2],
        program=user[3],
        email=user[4],
        bio=user[5],
        profile_pic=profile_pic
    )



# Denna funktion ser till att inloggad användare kan både lägga till och ta bort sparade inlägg.
@app.route("/toggle_favorite", methods=["POST"])
def toggle_favorite():
    """
    Denna funktion lägger till eller tar bort ett portfolioinlägg från användarens favoriter.

    Kräver att användaren är inloggad. Om inlägget redan är sparat tas det bort, 
    annars sparas det som favorit. Returnerar ett JSON-svar med status "added" 
    eller "removed" beroende på åtgärd.
    """

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Du måste vara inloggad."}), 403

    data = request.get_json()
    portfolio_id = data.get("portfolio_id")
    user_id = session["user_id"]

    if not portfolio_id:
        return jsonify({"success": False, "message": "Portfolio saknas."}), 400

    try:
        conn = connect_db()
        cur = conn.cursor()

        # Kontrollera om det redan är sparat
        cur.execute("SELECT 1 FROM saved_portfolios WHERE user_id = %s AND portfolio_id = %s", (user_id, portfolio_id))
        exists = cur.fetchone()

        if exists:
            cur.execute("DELETE FROM saved_portfolios WHERE user_id = %s AND portfolio_id = %s", (user_id, portfolio_id))
            conn.commit()
            status = "removed"
        else:
            cur.execute("INSERT INTO saved_portfolios (user_id, portfolio_id) VALUES (%s, %s)", (user_id, portfolio_id))
            conn.commit()
            status = "added"

        cur.close()
        conn.close()
        return jsonify({"success": True, "status": status})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500




# Säkerställer att fel meddelas under testning
if __name__ == "__main__":
    app.run(debug=True)