from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base
from utils import create_user, create_product_with_brand_and_category, create_order

DB_URL = "sqlite:///test.db"

engine = create_engine(DB_URL, echo=True)

Session = sessionmaker(bind=engine)


if __name__ == '__main__':
    # engine.echo = False
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.echo = True

    create_user(Session)
    create_product_with_brand_and_category(Session)
    create_order(Session)
