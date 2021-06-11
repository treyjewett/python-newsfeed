from os import getenv
from flask import g #type:ignore
from sqlalchemy.ext.declarative import declarative_base #type:ignore
from sqlalchemy import create_engine #type:ignore
from sqlalchemy.orm import sessionmaker #type:ignore
from dotenv import load_dotenv #type:ignore

load_dotenv()

#connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
  Base.metadata.create_all(engine)

  app.teardown_appcontext(close_db)

def get_db():
  if 'db' not in g:
    #store db connection in app context
    g.db = Session()

  return g.db

def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()