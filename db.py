from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    pass


class Product(Base):
    pass


class Category(Base):
    pass


class Brand(Base):
    pass


class Order(Base):
    pass


class OrderItem(Base):
    pass
