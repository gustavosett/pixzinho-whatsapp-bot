"""
    Esse código é responsável a criar e gerenciar
o banco de dados utilizando sqlalchemy.

author: github.com/gustavosett
"""

from contextlib import contextmanager
from os import getenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy_utils import database_exists, create_database

# Endereço
SQL_DATABASE_ALCHEMY_URL = getenv("DATABASE_URL")


# Conexão
engine = create_engine(
    SQL_DATABASE_ALCHEMY_URL,
    connect_args={
        # esse argumento só é necessário para SQLite:
        "check_same_thread": False
    },
)
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()


# configura WAL (Write-Ahead Logging)
@event.listens_for(engine, "connect")
def set_sqlite_wal_mode(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.close()


def initialize_db(need_to_create_system=False):
    """Atualiza/cria modelos e impede loops nas importações"""
    from app.db.session import Base, engine
    import app.db.models

    Base.metadata.create_all(bind=engine)
    # if need_to_create_system:
    #     from app.db.models import System

    #     create_system(SessionLocal, System)


def create_system(db, system_model):
    """cria sistema com configurações padrões"""
    new_system = system_model()
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    return new_system


# Dependencia
if not database_exists(engine.url):
    create_database(engine.url)
    initialize_db(need_to_create_system=True)

def get_db():
    """certifica que o banco de dados seja fechado ao final de cada request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """certifica que o banco de dados seja fechado ao final de cada request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()