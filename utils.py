from sqlalchemy.orm import sessionmaker

from db import User, Brand, Category, Product, Order


def create_user(session: sessionmaker, /, **kwargs) -> User:
    users_data = {
        "username": kwargs.get("username", "Test username"),
    }
    with session() as session:
        user = User(**users_data)
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def create_brand(session: sessionmaker, /, **kwargs) -> Brand:
    brand_data = {
        "name": kwargs.get("name", "Test brand"),
    }
    with session() as session:
        brand = Brand(**brand_data)
        session.add(brand)
        session.commit()
        session.refresh(brand)
    return brand


def create_category(session: sessionmaker, /, **kwargs) -> Category:
    category_data = {
        "name": kwargs.get("name", "Test category"),
    }
    with session() as session:
        category = Category(**category_data)
        session.add(category)
        session.commit()
        session.refresh(category)
    return category


def create_product_with_brand_and_category(session: sessionmaker, /, **kwargs) -> Product:
    brand_id = kwargs.get("brand_id", create_brand(session).id)
    category_id = kwargs.get("category_id", create_category(session).id)

    products_data = {
        "name": kwargs.get("name", "Test product"),
        "amount": kwargs.get("amount", 100),
        "price": kwargs.get("price", 145.00),
        "brand_id": kwargs.get("brand_id", brand_id),
        "category_id": kwargs.get("category_id", category_id),
    }

    with session() as session:
        product = Product(**products_data)
        session.add(product)
        session.commit()
        session.refresh(product)

    return product
