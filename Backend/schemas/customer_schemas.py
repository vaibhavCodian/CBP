import datetime
import datetime as _dt
import pydantic as _pydantic


class _CustomerBase(_pydantic.BaseModel):

    name: str
    email: _pydantic.EmailStr
    age: int = 20
    gender: str = 'Male'
    category: str = 'Unidentified'


class CustomerCreate(_CustomerBase):
    pass

class CustomerCreate2(_CustomerBase):
    date_created: _dt.datetime

class Customer(_CustomerBase):
    id: int
    date_created: _dt.datetime

    class Config:
        orm_mode = True


class _PurchaseBase(_pydantic.BaseModel):
    owner_id: int
    seller_id: int
    name: str
    category: str
    brand: str
    sold_by: str
    address: str
    date_created: _dt.datetime


class PurchaseCreate(_PurchaseBase):
    pass


class Purchase(_PurchaseBase):
    id: int

    class Config:
        orm_mode = True



