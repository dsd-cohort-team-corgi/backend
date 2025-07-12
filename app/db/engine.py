from dotenv import load_dotenv
from sqlmodel import create_engine
import os

load_dotenv() # takes environment variables


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True) # engine object allows us to talk to db, run queries, create tables, etc