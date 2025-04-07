import psycopg2
from config import get_database_url

try:
    conn = psycopg2.connect(get_database_url())
    print("Conexión exitosa con psycopg2")
    conn.close()
except Exception as e:
    print("Error de conexión:", e)
