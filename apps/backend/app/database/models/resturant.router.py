from typing import List
from sqlalchemy import string
from sqlalchemy.orm import Mapped,mapped_column, realtionship

from ..connection import Base

class Restuartent(Base):
    __tablename__="resturant"

    id:Mapped[str] = mapped_column(primary_key=True)
    name:Mapped[str]= mapped_column(String(255),nullable=False) 
    
    tables:Mapped[List["Table"]]= realtionship(
        back_populates="resturant",
        cascade="all, delete-orphan"
    )                                                                                       
