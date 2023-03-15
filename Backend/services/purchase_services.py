import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import Backend.database as _database, Backend.models as _models, Backend.schemas.purchase_schemas as _schemas
from Backend.config import settings


async def create_purchase(db: _orm.Session, purchase: _schemas.PurchaseCreate):
    purchase = _models.Purchase(**purchase.dict())
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return _schemas.Purchase.from_orm(purchase)


async def create_purchase2_gen(db: _orm.Session, purchase: _schemas.PurchaseCreate2):
    purchase = _models.Purchase(**purchase.dict())
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return _schemas.Purchase.from_orm(purchase)

async def get_purchases( db: _orm.Session):
    purchases = db.query(_models.Purchase).order_by(_models.Purchase.date_created.asc()).limit(200)

    return list(map(_schemas.Purchase.from_orm, purchases))


async def _purchase_selector(purchase_id: int, db: _orm.Session):
    purchase = (
        db.query(_models.Purchase)
        .filter(_models.Purchase.id == purchase_id)
        .first()
    )

    if purchase is None:
        raise _fastapi.HTTPException(status_code=404, detail="Purchase does not exist")

    return purchase


async def get_purchase(purchase_id: int, db: _orm.Session):
    purchase = await _purchase_selector(purchase_id=purchase_id, db=db)

    return _schemas.Purchase.from_orm(purchase)


async def delete_purchase(purchase_id: int, db: _orm.Session):
    purchase = await _purchase_selector(purchase_id, db)

    db.delete(purchase)
    db.commit()


async def update_purchase(purchase_id: int, purchase: _schemas.PurchaseCreate, db: _orm.Session):
    purchase_db = await _purchase_selector(purchase_id, db)

    purchase_db.seller_id = purchase.seller_id
    purchase_db.owner_id = purchase.owner_id
    purchase_db.name = purchase.name
    purchase_db.category = purchase.category
    purchase_db.brand = purchase.brand
    purchase_db.sold_by = purchase.sold_by
    purchase_db.address = purchase.address

    db.commit()
    db.refresh(purchase_db)

    return _schemas.Purchase.from_orm(purchase_db)





