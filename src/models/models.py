from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, Time, Double, DateTime

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),

)


security_trades = Table(
    "security_trades",
    metadata,
    Column("Security_Id", String, nullable=False),
    Column("Tradeno", Integer, primary_key=True),
    Column("Tradetime", Time, nullable=False),
    Column("Boardid", String, nullable=False),
    Column("Prise", Double, nullable=False),
    Column("Quantity", Integer, nullable=False),
    Column("Value", Double, nullable=False),
    Column("Period", String, nullable=False),
    Column("Yied", Double, nullable=False),
    Column("Tradetime_grp", Integer, nullable=False),
    Column("Systime", DateTime, nullable=False),
    Column("Buysell", String, nullable=False),
    Column("Decimals", Integer, nullable=False),
    Column("Tradingsession", String, nullable=False),

)

security = Table(
    "security",
    metadata,
    Column("NAME", String, primary_key=True),
)
