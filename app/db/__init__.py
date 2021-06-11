from os import getenv
from sqlalchemy.ext.declarative import declarative_base #type:ignore
from sqlalchemy import create_engine #type:ignore
from sqlalchemy.orm import sessionmaker #type:ignore
from dotenv import load_dotenv #type:ignore

load_dotenv()

#connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()