from typing import List

import fastapi as _fastapi
import sqlalchemy.orm as _orm

import Backend.schemas.customer_schemas as _schemas
import Backend.schemas.user_schemas as _UserSchemas
import Backend.services.customer_services as _services
import Backend.services.user_services as _UserService
import Backend.models as _models

router = _fastapi.APIRouter(
    prefix="/api/customer",
    tags=['Customer']
)


@router.post("/", status_code=_fastapi.status.HTTP_201_CREATED)
async def create_customer(
    customer: _schemas.CustomerCreate,
    user: _UserSchemas = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    return await _services.create_customer(db=db, customer=customer)


@router.get("/", response_model=List[_schemas.Customer])
async def get_customers(
    user: _UserSchemas = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    return await _services.get_customers(db=db)


@router.get("/total")
async def get_total_customers(
    user: _UserSchemas = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    count = db.query(_models.Customer).count()
    return count



@router.get("/{customer_id}", status_code=200)
async def get_customer(
    customer_id: int,
    user: _UserSchemas.User = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    return await _services.get_customer(customer_id, db)


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: int,
    user: _UserSchemas.User = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    await _services.delete_customer(customer_id, db)
    return {"message", "Successfully Deleted"}


@router.put("/{customer_id}", status_code=200)
async def update_customer(
    customer_id: int,
    customer: _schemas.CustomerCreate,
    user: _UserSchemas.User = _fastapi.Depends(_UserService.get_current_user),
    db: _orm.Session = _fastapi.Depends(_UserService.get_db),
):
    await _services.update_customer(customer_id, customer, db)
    return {"message", "Successfully Updated"}