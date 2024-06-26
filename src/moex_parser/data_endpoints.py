from fastapi import APIRouter, HTTPException, Depends, Request
from starlette import status as http_status

from databases import Database
from sqlalchemy import select, insert

from config import settings
from models.models import security_trades, security
from moex_parser.schemas import SecurityOut, SecurityTradeOut
from api.auth import get_user

router = APIRouter(tags=['data'])

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}"


async def get_database():
    database = Database(DATABASE_URL)
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()

async def create_security_trade(data: dict, database: Database):
    query = insert(security_trades).values(**data)
    await database.execute(query)
    query = select(security_trades).where(security_trades.c.Tradeno == data.get("Tradeno"))
    return await database.fetch_one(query)

async def get_security_trade(trade_number: int, database: Database):
    query = select(security_trades).where(security_trades.c.Tradeno == trade_number)
    return await database.fetch_one(query)

async def create_security(data: dict, database: Database):
    query = insert(security).values(**data)
    await database.execute(query)

async def get_security(name: str, database: Database):
    query = select(security).where(security.c.NAME == name)
    return await database.fetch_one(query)

@router.post(
    path='/security-trades',
    name='Create new security trade',
    status_code=http_status.HTTP_201_CREATED,
    response_model=SecurityTradeOut
)
async def create_security_trade_endpoint(data: SecurityTradeOut, request: Request, database: Database = Depends(get_database)):
    user = await get_user(request.state.user.get("email"), database)
    if user.role_id != 2:
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN)
    try:
        return await create_security_trade(data.dict(), database)
    except Exception as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    path='/security-trades/{trade_number}',
    name='Get security trade by Tradeno',
    status_code=http_status.HTTP_200_OK,
    response_model=SecurityTradeOut
)
async def get_security_trade_endpoint(trade_number: int, database: Database = Depends(get_database)):
    trade = await get_security_trade(trade_number, database)
    if trade is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Trade not found")
    return trade

@router.post(
    path='/security',
    name='Create new security',
    status_code=http_status.HTTP_201_CREATED
)
async def create_security_endpoint(data: dict, database: Database = Depends(get_database)):
    try:
        await create_security(data, database)
    except Exception as e:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path='/security/{name}',
    name='Get security by name',
    status_code=http_status.HTTP_200_OK,
    response_model=SecurityOut,
)
async def get_security_endpoint(name: str, database: Database = Depends(get_database)):
    sec = await get_security(name, database)
    if sec is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Security not found")
    return security


