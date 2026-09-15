from typing import TYPE_CHECKING,List
from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column, relationship

from ..connection import Base
if TYPE_CHECKING:
    from .table import table
    from .booking import booking
class Restaurant(Base):
    __tablename__="restaurant"

    id:Mapped[str] = mapped_column(primary_key=True)
    name:Mapped[str]= mapped_column(String(255),nullable=False) 
    
    tables:Mapped[List["table"]]= relationship(
        back_populates="resturant",
        cascade="all, delete-orphan"
    )                                                                                       
