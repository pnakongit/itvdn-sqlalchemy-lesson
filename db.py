from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    CheckConstraint,
    ForeignKey,
    Enum
)

import datetime
import enum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    email = Column(String(50), unique=True)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime(), default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime(),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )

    orders = relationship("Order", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class NameAbstract(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<NameAbstract(id={self.id}, name={self.name})>"


class Category(NameAbstract):
    __tablename__ = "category"

    products = relationship("Product", back_populates="category")


class Brand(NameAbstract):
    __tablename__ = "brand"

    products = relationship("Product", back_populates="brand")


class Product(NameAbstract):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    price = Column(
        Float(),
        CheckConstraint("price>=0", name="price_eg_0"),
        nullable=False,
        default=0
    )
    amount = Column(
        Integer(),
        CheckConstraint("amount>=0", name="amount_eg_0"),
        nullable=False,
        default=0
    )
    brand_id = Column(Integer, ForeignKey("brand.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name})"

    @property
    def is_available(self) -> bool:
        return self.amount > 0


class Order(Base):
    class Status(enum.Enum):
        NEW = "new"
        IN_PROGRESS = "in progress"
        COMPLETED = "completed"

    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=datetime.datetime.utcnow, nullable=False)
    status = Column(Enum(Status, create_constraint=True), nullable=False, default=Status.NEW)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id})>"


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True)
    amount = Column(
        Integer,
        CheckConstraint("amount>=0", name="amount_eg_0"),
        nullable=False,
        default=0
    )

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, product_id={self.product_id})>"
