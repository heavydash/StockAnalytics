from fastapi import APIRouter, HTTPException, Depends
from starlette import status as http_status

from databases import Database
from sqlalchemy import insert, select

from auth.schemas import RegistrationIn, LoginIn
from models.models import user

router = APIRouter(prefix='/auth', tags=['auth'])

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"


async def create_user(data: dict, database: Database):
    query = insert(user).values(**data, is_active=True, is_verified=False, is_superuser=False)
    await database.execute(query)

async def get_user(email: str, database: Database):
    query = select(user).where(user.c.email == email)
    return await database.fetch_one(query)

def is_password_valid(input_password: str, user_password: str) -> bool:
    return input_password == user_password

async def get_database():
    database = Database(DATABASE_URL)
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()


@router.post(
    path='/register',
    name='Create new auth',
    status_code=http_status.HTTP_201_CREATED
)
async def register_in(data: RegistrationIn, database: Database = Depends(get_database)):
    try:
        await create_user(data.dict(), database)
    except Exception as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    path='/login',
    name='Login user',
    status_code=http_status.HTTP_200_OK
)
async def login_in(data: LoginIn, database: Database = Depends(get_database)):
    #try:
    db_user = await get_user(data.email, database)
    if db_user is None:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")
    if not is_password_valid(data.hashed_password, db_user.hashed_password):
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")
    # except Exception as e:
    #     raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))
