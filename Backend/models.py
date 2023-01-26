import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    sold = _orm.relationship("Purchase", back_populates="seller")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Customer(_database.Base):
    __tablename__ = "customers"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    gender = _sql.Column(_sql.String, index=True, default="Other")
    age = _sql.Column(_sql.Integer, index=True, default="18")
    category = _sql.Column(_sql.String, index=True, default="Other")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow())
    purchases = _orm.relationship("Purchase", back_populates="owner")


class Purchase(_database.Base):
    __tablename__ = "purchases"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    seller_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("customers.id"))
    name = _sql.Column(_sql.String, index=True)
    price = _sql.Column(_sql.Float, index=True)
    quantity = _sql.Column(_sql.Integer, index=True)
    category = _sql.Column(_sql.String, index=True, default="Other")
    brand = _sql.Column(_sql.String, index=True, default="Other")
    address = _sql.Column(_sql.String, index=True, default="in-store")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow())
    owner = _orm.relationship("Customer", back_populates="purchases")
    seller = _orm.relationship("User", back_populates="sold")

_database.Base.metadata.create_all(bind=_database.engine)