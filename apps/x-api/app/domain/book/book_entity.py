from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Book(SQLModel, table=True):
    """This class represents a book in the database"""

    __tablename__ = "books"

    uid: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    title: str
    author: str
    isbn: str = Field(sa_column=Column(pg.VARCHAR, unique=True))
    description: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self) -> str:
        """Returns a string representation of the book instance."""
        return f"<Book(uid={self.uid}, title={self.title}, author={self.author})>"
