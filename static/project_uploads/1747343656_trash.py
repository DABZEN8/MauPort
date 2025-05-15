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
    - Skapa ny artikel
    - 6 artiklar 
    """
    return "<h1>Min fantastiska Wiki!</h1>"

@route("/1")
def first_article():
    """Första artikeln, inkl. möjlighet att redigera artikeln."""

@route("/2")
def second_article():
    """Andra artikeln, inkl. möjlighet att redigera artikeln."""

@route("/3")
def second_article():
    """Tredje artikeln, inkl. möjlighet att redigera artikeln."""

@route("/4")
def second_article():
    """Fjärde artikeln, inkl. möjlighet att redigera artikeln."""

@route("/5")
def second_article():
    """Femte artikeln, inkl. möjlighet att redigera artikeln."""

@route("/6")
def second_article():
    """Sjätte artikeln, inkl. möjlighet att redigera artikeln."""

@route("/NewArticle", method="POST") # Skapa ny artikel med metoden POST
def new_article():
    """Möjlighet för användare att skapa en ny artikel, läggs till i slutet av listan."""



# Kör programmet i webbläsaren
run(host="127.0.0.1", port=8080, debug=False, reloader=True) 