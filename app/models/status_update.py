import enum
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Column, DateTime, Field, SQLModel, text


class StatusEnum(str, enum.Enum):
    confirmed = "confirmed"
    en_route = "en_route"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class StatusUpdateBase(SQLModel):
    booking_id: UUID
    status: Optional[StatusEnum]


class StatusUpdate(StatusUpdateBase, table=True):
    __tablename__ = "status_updates"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=text("(now() AT TIME ZONE 'utc')")
        ),
    )


class StatusUpdateCreate(StatusUpdateBase):
    pass


class StatusUpdateUpdate(SQLModel):
    status: Optional[StatusEnum] = None
