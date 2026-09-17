from typing import TYPE_CHECKING,List
from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column, relationship
if TYPE_CHECKING:
        from .table import Table
        from .booking import Booking
from ..connection import Base

class Restaurant(Base):
    __tablename__="restaurant"

    id:Mapped[str] = mapped_column(primary_key=True)
    name:Mapped[str]= mapped_column(String(255),nullable=False) 
    
    tables:Mapped[List["Table"]]= relationship(
        "Table",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )                                                                                       
