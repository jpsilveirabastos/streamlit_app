from .config import DBNAME, USER, PASSWORD, HOST
import psycopg2

class Db_pg:
    
    def connect():
        print(DBNAME, USER)
        conn = psycopg2.connect(dbname='st-data', user='st-app', password='Mel4ncia24', host='/cloudsql/streamlit-app-395600:us-central1:st-app')
        cur = conn.cursor()
        return cur, conn

    def disconnect(cur, conn):
        cur.close()
        conn.close()