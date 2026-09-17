from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.restaurant import RestaurantCreate,RestaurantResponse
from app.database.models.restaurant import Restaurant


router = APIRouter(
    prefix="/restaurant"
    tags=["Restaurant"]
    )


@router.post("/",response_model=RestaurantResponse)
def create_restaurant(
    restaurant: RestaurantCreate,
    db:Session=Depends(get_db)
):
    new_restaurant=Restaurant(
        name=restaurant.name
    )

            
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant
