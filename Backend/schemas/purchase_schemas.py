import datetime
import datetime as _dt
import pydantic as _pydantic
from ..schemas.customer_schemas import Customer as _Customer
from ..schemas.user_schemas import User as _User


class _PurchaseBase(_pydantic.BaseModel):
    owner_id: int
    seller_id: int
    name: str
    category: str
    quantity: int
    price: float
    brand: str
    address: str


class PurchaseCreate(_PurchaseBase):
    pass


class Purchase(_pydantic.BaseModel):
    id: int
    name: str
    category: str
    brand: str
    quantity: int
    price: float
    quantity: int
    address: str
    owner: _Customer
    seller: _User
    date_created: datetime.datetime

    class Config:
        orm_mode = True





