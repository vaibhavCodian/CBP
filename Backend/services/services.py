import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import Backend.database as _database, Backend.schemas as _schemas
from Backend.config import settings


oauth2schema = _security.OAuth2PasswordBearer(tokenUrl='/api/token')


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
