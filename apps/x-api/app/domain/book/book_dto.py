from pydantic import BaseModel

from .book_entity import Book


class BookResult(Book):
    """This class is used to validate the response when getting book objects"""
    #pass #Commenting out pass as suggested by lint


class BookCreateForm(BaseModel):
    """This class is used to validate the request when creating or updating a book"""

    title: str
    author: str
    isbn: str
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sapiens: A Brief History of Humankind",
                "author": "Yuval Noah Harari",
                "isbn": "978-0099590088",
                "description": """Earth is 4.5 billion years old.""",
            }
        }
    }
