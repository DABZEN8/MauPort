import psycopg2 as psql
import configparser

def connect_db():
    """Anslut till PostgreSQL-databasen och returnera anslutningen. Vi referar till säkerhetsnycklar
    från vå text fil."""
    config = configparser.ConfigParser()
    config.read('config.ini')

    db_config = {
        'host': config['database']['host'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'dbname': config['database']['database']
    }

    try:
        connection = psql.connect(**db_config)
        return connection
    except Exception as e:
        print("Fel vid anslutning till databasen:", e)
        return None