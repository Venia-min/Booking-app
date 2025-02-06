from datetime import date

from pydantic import BaseModel


class SBooking(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int  # for room
    name: str  # for room
    description: str  # for room
    services: str  # for room

    class Config:
        from_attributes = True
