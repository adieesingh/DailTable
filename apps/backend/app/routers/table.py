import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models.restaurant import Restaurant
from app.database.models.table import Table
from app.schemas.table import TableCreate, TableResponse

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.post(
    "",
    response_model=TableResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new table",
)
def create_table(
    payload: TableCreate,
    db: Session = Depends(get_db),
):
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == payload.restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id '{payload.restaurant_id}' does not exist",
        )

    table_id = payload.id or str(uuid.uuid4())

    existing = db.query(Table).filter(Table.id == table_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Table with id '{table_id}' already exists",
        )

    table = Table(
        id=table_id,
        restaurant_id=payload.restaurant_id,
        capacity=payload.capacity,
    )
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@router.get(
    "",
    response_model=List[TableResponse],
    summary="List tables",
)
def list_tables(
    restaurant_id: Optional[str] = Query(default=None, description="Filter tables by restaurant ID"),
    limit: int = Query(default=100, ge=1, le=1000, description="Max number of items to return"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    db: Session = Depends(get_db),
):
    query = db.query(Table)
    if restaurant_id:
        query = query.filter(Table.restaurant_id == restaurant_id)

    tables = query.offset(offset).limit(limit).all()
    return tables


@router.get(
    "/{table_id}",
    response_model=TableResponse,
    summary="Get a table by ID",
)
def get_table(
    table_id: str,
    db: Session = Depends(get_db),
):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id '{table_id}' not found",
        )
    return table
