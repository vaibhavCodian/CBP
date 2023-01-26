from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm

import Backend.services.user_services as _services
import Backend.schemas.user_schemas as _schemas



router = _fastapi.APIRouter(
    prefix="/api/user",
    tags=['User']
)


@router.get("/", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@router.post("/", status_code=_fastapi.status.HTTP_201_CREATED)
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)
