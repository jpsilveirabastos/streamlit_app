import os
from dotenv import load_dotenv

load_dotenv()

DBNAME = os.getenv('DBNAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
TESTE = os.getenv('TESTE')

print(DBNAME, TESTE)