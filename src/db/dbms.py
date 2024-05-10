from copy import deepcopy
from datetime import timedelta
from typing import Any, Iterable, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

sqlalchemy_database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user='postgres',
    password='postgres',
    host='0.0.0.0',
    port=5432,
    path="/postgres",
)

engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


class ManagerBase:

    def __init__(self, session: AsyncSession):
        self.session = session

    def execute(self, query):
        return self.session.execute(query)

    async def update(self, instance: ModelType, data_update: Union[UpdateSchemaType, dict[str, Any]]):
        if not isinstance(data_update, dict):
            data_update = data_update.dict(exclude_unset=True)

        for field in jsonable_encoder(data_update):
            setattr(instance, field, data_update.get(field))

        self.session.add(instance)
        await self.session.commit()

        return instance

    async def create(self, model: Type[ModelType], data_create: CreateSchemaType):
        data_create = jsonable_encoder(data_create)
        instance = model(**data_create)
        self.session.add(instance)
        await self.session.commit()

        return instance

    async def add_all(self, instances: Iterable[ModelType]) -> Iterable[ModelType]:
        self.session.add_all(instances)
        await self.session.commit()

        return instances

    async def delete(self, instance: ModelType):
        await self.session.delete(instance)
        await self.session.commit()

        return instance
