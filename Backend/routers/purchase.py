from typing import List

import fastapi as _fastapi
import sqlalchemy.orm as _orm

import Backend.schemas.purchase_schemas as _schemas
import Backend.schemas.user_schemas as _UserSchemas
import Backend.services.purchase_services as _services
import Backend.services.user_services as _UserService
import Backend.services.customer_services as _CustomerService

router = _fastapi.APIRouter(
    prefix="/api/purchase",
    tags=['Purchase']
)


@router.post("/", status_code=_fastapi.status.HTTP_201_CREATED, response_model=_schemas.Purchase)
async def create_purchase(
    purchase: _schemas.PurchaseCreate,
    user: _UserSchemas = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    # # get customer by email
    # db_customer = await _CustomerService.get_customer_by_email(purchase.email, db)
    #
    # if not db_customer:
    #     raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    # purchase.owner_id
    print(purchase)
    return await _services.create_purchase(db=db, purchase=purchase)


@router.post("/2", status_code=_fastapi.status.HTTP_201_CREATED, response_model=_schemas.Purchase)
async def create_purchase2_gen(
    purchase: _schemas.PurchaseCreate2,
    user: _UserSchemas = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    print(purchase)
    return await _services.create_purchase2_gen(db=db, purchase=purchase)

@router.get("/", response_model=List[_schemas.Purchase])
async def get_purchases(
    user: _UserSchemas = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    return await _services.get_purchases(db=db)


@router.get("/{purchase_id}", status_code=200)
async def get_purchase(
    purchase_id: int,
    user: _UserSchemas.User = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    return await _services.get_purchase(purchase_id, db)


@router.delete("/{purchase_id}", status_code=204)
async def delete_purchase(
    purchase_id: int,
    user: _UserSchemas.User = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    await _services.delete_purchase(purchase_id, db)
    return {"message", "Successfully Deleted"}


@router.put("/{purchase_id}", status_code=200)
async def update_purchase(
    purchase_id: int,
    purchase: _schemas.PurchaseCreate,
    user: _UserSchemas.User = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    await _services.update_purchase(purchase_id, purchase, db)
    return {"message", "Successfully Updated"}