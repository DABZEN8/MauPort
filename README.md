# Slutinlämning - Projektversion 1.0

## Innehåll:
Slutversionen av projektet finns som en release under titeln "slutversion_mauport" där all relevant kod finns för att köra programmet.

## Krav:
- Python 3.10 eller högre
- PostgreSQL (installerad lokalt eller via t.ex. pgAdmin)
- Internetanslutning för att ladda externa bibliotek (vid behov)
- Om man vill köra programmet och öppna webbsidan behöver vissa paket installeras. I terminalen kan man skriva följande: "pip install flask werkzeug flask-wtf wtforms psycopg2-binary python-dotenv" och klicka enter så att alla relevanta paket installeras.

## Databas
Applikationen använder en PostgreSQL-databas. För att skapa tabellerna, kör skriptet db/create_schema.sql via terminalen:
psql -U postgres -d mauport -f db/create_schema.sql
Eller alternativt, kopiera all skript från create_schema.sql och klistra in det i en egen pgadmin databas.

## .env
- db_host
- db_database
- db_user
- db_password

## Hur man kör koden:
1. Ladda upp mappen från ZIP-filen till din dator.
2. Öppna filerna i **Visual Studio Code** eller annan kodredigerare.
3. Kör programmet via terminalen (t.ex. python app.py eller flask run beroende på setup).
4. Gå till [http://127.0.0.1:5000](http://127.0.0.1:5000) i din webbläsare för att använda applikationen.

## Länkar till kod:
- **Kodens repository på GitHub**: [MauPort GitHub Repository](https://github.com/DABZEN8/MauPort)