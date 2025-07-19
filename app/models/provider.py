from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, DateTime, text

class ProviderBase(SQLModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[int] = None

# Full model for DB
class Provider(ProviderBase, table=True):
    __tablename__ = "providers"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("(now() AT TIME ZONE 'utc')"))
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("(now() AT TIME ZONE 'utc')"))
    )


# Schema for create
class ProviderCreate(SQLModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[int] = None
    user_id: UUID

# Schema for update
class ProviderUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[int] = None
