from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    


class RestaurantResponse(BaseModel):
    id:str
    name:str

    model_config={
        "from_attributes": True
    }