import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantResponse

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new restaurant",
)
def create_restaurant(
    payload: RestaurantCreate,
    db: Session = Depends(get_db),
):
    restaurant_id = payload.id or str(uuid.uuid4())

    existing = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Restaurant with id '{restaurant_id}' already exists",
        )

    restaurant = Restaurant(
        id=restaurant_id,
        name=payload.name,
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.get(
    "",
    response_model=List[RestaurantResponse],
    summary="List all restaurants",
)
def list_restaurants(
    limit: int = Query(default=100, ge=1, le=1000, description="Max number of items to return"),
    offset: int = Query(default=0, ge=0, description="Number of items to skip"),
    db: Session = Depends(get_db),
):
    restaurants = db.query(Restaurant).offset(offset).limit(limit).all()
    return restaurants


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    summary="Get a restaurant by ID",
)
def get_restaurant(
    restaurant_id: str,
    db: Session = Depends(get_db),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id '{restaurant_id}' not found",
        )
    return restaurant
