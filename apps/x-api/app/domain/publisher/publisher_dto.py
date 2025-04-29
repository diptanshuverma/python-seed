from pydantic import BaseModel

from .publisher_entity import Publisher


class PublisherResult(Publisher):
    """This class is used to validate the response when getting publisher objects"""
    #pass #Commenting out pass as suggested by lint


class PublisherCreateForm(BaseModel):
    """This class is used to validate the request when creating or updating a publisher"""

    publisher_id: int
    publisher_name: str
    location: str
    registration_id: str
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
            "publisher_id": 105,
            "publisher_name": "Wildlife Books",
            "location": "Madagascar",
            "registration_id": "REG0672",
            "description": "Only Madagascar-based book publisher."
    }
        }
    }
