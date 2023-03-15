import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import Backend.database as _database, Backend.models as _models, Backend.schemas.customer_schemas as _schemas
from Backend.config import settings


async def create_customer(db: _orm.Session, customer: _schemas.CustomerCreate):
    customer = _models.Customer(**customer.dict())
    print(str(db.add(customer)))
    db.commit()
    db.refresh(customer)

    return _schemas.Customer.from_orm(customer)


async def create_customer2gen(db: _orm.Session, customer: _schemas.CustomerCreate2):
    customer = _models.Customer(**customer.dict())
    print(str(db.add(customer)))
    db.commit()
    db.refresh(customer)

    return _schemas.Customer.from_orm(customer)


async def get_customers( db: _orm.Session):
    customers = db.query(_models.Customer).order_by(_models.Customer.date_created.desc()).limit(200)
    print(str(customers))
    return list(map(_schemas.Customer.from_orm, customers))


async def _customer_selector(customer_id: int, db: _orm.Session):
    customer = (
        db.query(_models.Customer)
        .filter(_models.Customer.id == customer_id)
        .first()
    )

    if customer is None:
        raise _fastapi.HTTPException(status_code=404, detail="Customer does not exist")

    return customer


async def get_customer_by_email(email: str, db: _orm.Session):
    return db.query(_models.Customer).filter(_models.Customer.email == email).first()


async def get_customer(customer_id: int, db: _orm.Session):
    customer = await _customer_selector(customer_id=customer_id, db=db)

    return _schemas.Customer.from_orm(customer)


async def delete_customer(customer_id: int, db: _orm.Session):
    customer = await _customer_selector(customer_id, db)

    db.delete(customer)
    db.commit()


async def update_customer(customer_id: int, customer: _schemas.CustomerCreate, db: _orm.Session):
    customer_db = await _customer_selector(customer_id, db)

    customer_db.name = customer.name
    customer_db.email = customer.email
    customer_db.age = customer.age
    customer_db.gender = customer.gender
    customer_db.category = customer.category

    db.commit()
    db.refresh(customer_db)

    return _schemas.Customer.from_orm(customer_db)
