import psycopg2 as psql
import os
from dotenv import load_dotenv

def connect_db():
    """Anslut till PostgreSQL-databasen och returnera anslutningen. Vi referar till säkerhetsnycklar
    från vå text fil."""
    load_dotenv()

    db_config = {
        'db_host': os.getenv('db_host'),
        'db_user': os.getenv('db_user'),
        'db_password': os.getenv('db_password'),
        'db_name': os.getenv('db_name')
    }

    try:
        connection = psql.connect(**db_config)
        return connection
    except Exception as e:
        print("Fel vid anslutning till databasen:", e)
        return None