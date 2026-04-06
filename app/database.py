import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

from app.config import INSTANCE_DIR, DATABASE_FILE

os.makedirs(INSTANCE_DIR, exist_ok=True)
engine = create_engine(f"sqlite:///{DATABASE_FILE.as_posix()}", connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def init_db():
    import app.models.user
    import app.models.verification
    Base.metadata.create_all(bind=engine)

def get_session():
    global session
    sessionlocal = session()
    try:
        yield sessionlocal
    finally:
        sessionlocal.close()
