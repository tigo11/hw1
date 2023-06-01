from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from .sqlalchemy_models import Base

load_dotenv()
POSTGRESQL_ENGINE_URL = os.environ.get('POSTGRESQL_ENGINE_URL')


def create_db_if_not_exists(database_uri: str):
    engine = create_engine(database_uri)
    if not database_exists(engine.url):
        create_database(engine.url)


def create_session():
    create_db_if_not_exists(POSTGRESQL_ENGINE_URL)
    engine = create_engine(POSTGRESQL_ENGINE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def delete_db():
    engine = create_engine(POSTGRESQL_ENGINE_URL)
    if database_exists(engine.url):
        drop_database(engine.url)