from bottle import run, route
import json

def JSON():
    # Öppna JSON-filen och läs in artiklar
    try:
        articles_file = open("static/info.json", "r")
        # Läser och konverterar innehållet från JSON filen till Python datatyp
        articles = json.loads(articles_file.read())
        # Stänger filen
        articles_file.close()
        # Returnerar artiklarna

        return articles

    # Skapa ny JSON-fil om det inte finns någon
    except:
        # Skapar ny fil som heter info.json
        articles_file = open("static/info.json", "w") # Skriver strukturen i JSON-format

@route("/") # Definierar vilken sida användaren ska dirigeras till, i detta fall startsidan
def index():
    """Förstasidan som innehåller följande:
    - Rubrik
    - Knapp - Skapa ny artikel
    - Lista över 6 artiklar 
    """
    return "<h1>Min fantastiska Wiki!</h1>"

@route("/<title>")
def read_articles():
    """Artiklarna, inkl. möjlighet att redigera artikeln."""

@route("/NewArticle", method="POST") # Skapa ny artikel med metoden POST
def new_article():
    """Möjlighet för användare att skapa en ny artikel, läggs till i slutet av listan."""


# Kör programmet i webbläsaren
run(host="127.0.0.1", port=8080, debug=False, reloader=True) 