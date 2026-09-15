from typing import TYPE_CHECKING,List
from sqlalchemy import ForeignKey,Integer, String
from sqlalchemy.orm import Mapped,mapped_column, relationship                       
from ..connection import Base
if TYPE_CHECKING:
    from .restaurant import Restaurant
    from .booking import Booking
class Table(Base):
    __tablename__="tables"
    id: Mapped[str] = mapped_column(String, primary_key=True)

    restaurant_id: Mapped[str] = mapped_column(
        ForeignKey("restaurant.id"),
        nullable=False,
    )

    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="tables"
    )

    bookings: Mapped[List["Booking"]] = relationship(
        back_populates="table",
        cascade="all, delete-orphan",
    )
