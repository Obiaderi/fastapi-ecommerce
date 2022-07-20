from typing import Optional
from pydantic import BaseModel


class SignupSchema(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "username": "Johndoe",
                "email": "johndoe@gamil.com",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = 'f4ea2ba25ca216fd4491a1c881d6e08b3ebf9d3c1d1928248cc2db0d26eb7ae5'


class LoginSchema(BaseModel):
    username: str
    password: str


class OrderSchema(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    user_id: Optional[int]

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE",
            }
        }


class OrderStatusSchema(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True

    schema_extra = {
        "example": {
            "order_status": "PENDING",
        }
    }


class CrudTextSchema(BaseModel):
    name: str
    language: str

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "name": "Johndoe Chief",
                "language": "English",
            }
        }
