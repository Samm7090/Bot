from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------
"Use mysql.connector for quick tests, admin scripts, or one-off tasks."
# -------------------------------------

def get_db_connection(host: str = 'localhost', user: str = 'root', password: str = None, database: str = None):
    if password is None:
        password = os.getenv('DB_PASS')
    if database is None:
        database= os.getenv('DB_Name')
    
    return mysql.connector.connect(host=host, user=user, password=password, database=database)


# -------------------------------------
"Use SQLAlchemy for production apps, APIs, and integration with frameworks like FastAPI, Flask, or Streamlit."
# -------------------------------------

def get_sqlalchemy_engine(host: str = 'localhost', user: str = 'root', password: str = None, database: str = None,connector: str = "mysqlconnector"):
    if password is None:
        password = os.getenv('DB_PASS')
    if database is None:
        database= os.getenv('DB_Name')
    
    # Encode password to handle special characters
    encoded_password = quote_plus(password)

    url=f"mysql+{connector}://{user}:{encoded_password}@{host}/{database}"
    engine=create_engine(url)

    return engine