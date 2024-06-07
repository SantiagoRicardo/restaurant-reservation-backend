import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# Configuración de la base de datos usando variables de entorno
host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
port = os.getenv('MYSQL_PORT')
db = os.getenv('MYSQL_DATABASE')


connectMySQL = mysql.connector.connect(user=user, password=password, host=host, database=db, port=port)

print(connectMySQL)
