"To set a Connection of MySQL Database and review data"

import mysql.connector
import pandas as pd

# Replace with your actual credentials
config = {
    'host': 'localhost',
    'user': 'root',         # or whatever username you use
    'password': 'Sam@4414',  # replace this
    'database': 'hrms'
}

conn = mysql.connector.connect(**config)

query = "SELECT * FROM employees;"
df = pd.read_sql(query, conn)
conn.close()

print(df.head())

#-----------------------------------------------------
"To load data from MySQL Database using LangChain"
#-----------------------------------------------------
from langchain_community.document_loaders import SQLDatabaseLoader
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus


load_dotenv()

# Fetch from .env
# If your password contains @, :, / or spaces, Python/SQLAlchemy will misinterpret it as part of the host or database, causing errors
# quote_plus solves this by encoding the password safely
password = quote_plus(os.getenv("DB_PASS"))

# Create SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost/hrms")

# Create SQLDatabase instance
db = SQLDatabase(engine)

# Load data using LangChain's SQLDatabaseLoader
loader = SQLDatabaseLoader(
    query="SELECT * FROM employees;",  # Adjust the query as needed
    db=db
)

docs = loader.load()
# Check loaded docs
print(f"✅ Loaded {len(docs)} employee records.")
print(docs[0].page_content[:500])  # Show a sample
