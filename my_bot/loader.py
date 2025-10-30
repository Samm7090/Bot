from langchain_community.document_loaders import SQLDatabaseLoader
from langchain_community.utilities.sql_database import SQLDatabase

def load_sql_data(query: str,engine):

    db= SQLDatabase(engine)
    loader= SQLDatabaseLoader(query=query, db=db)
    docs = loader.load()

    return docs