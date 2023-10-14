from .config import DBNAME, USER, PASSWORD, HOST
import psycopg2

class Db_pg:
    
    def connect():
        print(DBNAME, USER)
        conn = psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST)
        cur = conn.cursor()
        return cur, conn

    def disconnect(cur, conn):
        cur.close()
        conn.close()