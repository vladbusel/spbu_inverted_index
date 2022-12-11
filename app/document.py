import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dotenv import dotenv_values

config = dotenv_values("../.env")

class Document:
    engine = create_engine(f'postgresql://postgres:{config["pg_password"]}@localhost/postgres')

    @classmethod
    def all(cls, collection_size = None):
        if collection_size == None:
            return pd.read_sql_query("SELECT * FROM documents", Document.engine)
        else:
            return pd.read_sql(text("""SELECT * FROM documents LIMIT {}""".format(collection_size)), Document.engine)

    @classmethod
    def find_by_id(cls, id):
        return pd.read_sql_query(text("""SELECT * FROM documents WHERE id = :id  LIMIT 1"""), Document.engine, params={"id":id})

    @classmethod
    def find_by_ids(cls, ids):
        return pd.read_sql(text("""SELECT * FROM documents WHERE id IN ({})""".format(','.join([str(id) for id in ids]))),
                                 Document.engine)
