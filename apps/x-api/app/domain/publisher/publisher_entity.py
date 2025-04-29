from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Publisher(SQLModel, table=True):
    """This class represents a publisher in the database"""

    __tablename__ = "publishers"

    uid: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    publisher_id: int
    publisher_name: str
    location: str
    registration_id: str
    description: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self) -> str:
        """Returns a string representation of the publisher instance."""
        return f"<Publisher(uid={self.uid}, title={self.title}, author={self.author})>"
