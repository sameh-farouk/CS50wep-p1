from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import psycopg2
from contextlib import contextmanager

class DbHelper:
    
    conn_string = os.getenv("DATABASE_URL") if os.getenv("DATABASE_URL") else None

    def __init__(self, conn_string=None):
        if not conn_string and not self.conn_string:
            raise RuntimeError("DATABASE_URL is not set")
        self.engine = create_engine(conn_string or self.conn_string)
        self.db_session = scoped_session(sessionmaker(bind=self.engine))

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.db_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def close_connection(self):
        self.engine.dispose()
    

db = DbHelper()
engine = db.engine
session = db.db_session() # session.execute
context_session = db.session_scope # with context_session() as session:
