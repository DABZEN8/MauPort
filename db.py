import psycopg2 as psql
import os
from dotenv import load_dotenv

def connect_db():
    """Anslut till PostgreSQL-databasen och returnera anslutningen. Vi referar till säkerhetsnycklar
    från vår text fil."""
    load_dotenv()

    db_config = {
        'host': os.getenv('db_host'),
        'database': os.getenv('db_database'),
        'user': os.getenv('db_user'),
        'password': os.getenv('db_password')
    }
    
    try:
        connection = psql.connect(**db_config)
        return connection
    except Exception as e:
        print("Fel vid anslutning till databasen:", e)
        return None
    
# def get_user_by_id(user_id):
#     conn = connect_db()
#     cur = conn.cursor()
#     cur.execute("SELECT username, profile_pic FROM users WHERE id = %s", (user_id,))
#     user = cur.fetchone()
#     cur.close()
#     conn.close()
#     return user