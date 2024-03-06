import datetime
import enum
from typing import List

from feedback.services import check_sentiment
from products.schema import UpdateProductSchema
from sqlalchemy import TIMESTAMP, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
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

    feedbacks: Mapped[List["FeedBack"]] = relationship(
        back_populates="product",
        cascade="all, delete",
    )

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

    @classmethod
    def get_feedbacks_for_product(cls, id: int, session: Session):
        stmt = select(cls).where(cls.id == id)
        product = session.scalars(stmt).first()
        return product.feedbacks


class Sentiments(enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class FeedBack(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    sentiment: Mapped[Sentiments]

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE")
    )

    product: Mapped["Product"] = relationship(back_populates="feedbacks")

    @classmethod
    def get_by_id(cls, id: int, session: Session):
        stmt = select(cls).where(cls.id == id)
        feedback = session.scalars(stmt).first()
        return feedback

    @classmethod
    def get_list(cls, session: Session):
        stmt = select(cls)
        feedbacks = session.scalars(stmt).all()
        return feedbacks

    @classmethod
    def delete_by_id(cls, id: int, session: Session):
        stmt = select(cls).where(cls.id == id)
        feedback = session.scalars(stmt).first()
        if feedback:
            session.delete(feedback)
            session.commit()
            return True
        else:
            return None

    @classmethod
    def create(
        cls,
        session: Session,
        product_id: int,
        text: str,
    ):
        product = Product.get_by_id(id=product_id, session=session)
        if product:
            sentiment = check_sentiment(text)
            feedback = cls(product_id=product_id, text=text, sentiment=sentiment)
            session.add(feedback)
            session.commit()
            return feedback
        else:
            return None
