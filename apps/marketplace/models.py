import datetime

from products.schema import UpdateProductSchema
from sqlalchemy import TIMESTAMP, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())

    @classmethod
    def get_by_id(cls, id: int, session: Session):
        stmt = select(cls).where(cls.id == id)
        product = session.scalars(stmt).first()
        return product

    @classmethod
    def get_list(cls, session: Session):
        stmt = select(cls)
        products = session.scalars(stmt).all()
        return products

    @classmethod
    def update_by_id(cls, id: int, new_product: UpdateProductSchema, session: Session):
        stmt = select(cls).where(cls.id == id)
        product = session.scalars(stmt).first()
        if product:
            for field, value in new_product.model_dump().items():
                if value is not None:
                    setattr(product, field, value)

            session.commit()
            return product
        else:
            return None

    @classmethod
    def delete_by_id(cls, id: int, session: Session):
        stmt = select(cls).where(cls.id == id)
        product = session.scalars(stmt).first()
        if product:
            session.delete(product)
            session.commit()
            return True
        else:
            return None

    @classmethod
    def get_or_create_by_name(
        cls,
        session: Session,
        name: str,
    ):
        stmt = select(cls).where(cls.name == name)
        product = session.scalars(stmt).first()
        if not product:
            product = cls(name=name)
            session.add(product)
            session.commit()
        return product
