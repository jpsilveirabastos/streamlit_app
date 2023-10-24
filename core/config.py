import os
from dotenv import load_dotenv

load_dotenv()

TESTE_VAR = os.environ.get("TESTE_VAR")
DBNAME = os.getenv('DBNAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')

