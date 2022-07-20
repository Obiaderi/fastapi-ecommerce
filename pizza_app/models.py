from datetime import datetime
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, String, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from pizza_app.database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True)
    email = Column(String(100), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.now,
                        default=datetime.utcnow)
    orders = relationship("OrderModel", back_populates="user")
    # This will return Str of username

    def __repr__(self) -> str:
        return f"<UserModel {self.username}"


class OrderModel(Base):

    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(
        choices=ORDER_STATUSES), default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), default="SMALL")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.now,
                        default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserModel", back_populates="orders")

    # This will return Str of username

    def __repr__(self) -> str:
        return f"<OrderModel {self.id}"


class UserTextModel(Base):
    __tablename__ = 'crud_text'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25), unique=True)
    language = Column(String(255))

    def __repr__(self) -> str:
        return f"<UserTextModel {self.username}"
