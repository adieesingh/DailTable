from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..connection import Base

if TYPE_CHECKING:
    from .table import Table


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    table_id: Mapped[str] = mapped_column(
        ForeignKey("tables.id"),
        nullable=False,
    )

    guest_name: Mapped[str] = mapped_column(String(255), nullable=False)

    guest_phone: Mapped[str] = mapped_column(String(20), nullable=False)

    party_size: Mapped[int] = mapped_column(Integer, nullable=False)

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="confirmed",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    table: Mapped["Table"] = relationship(
        back_populates="bookings"
    )