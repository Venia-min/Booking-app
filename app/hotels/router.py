from datetime import date
from typing import List

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import HotelNotAvailableException
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SSingleHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}")
@cache(expire=30)
async def get_available_hotels(
    location: str,
    date_from: date,
    date_to: date,
) -> List[SHotel]:
    """
    Returns a list of hotels, must have at least 1 free room.
    Requires authorization: no.
    :param location:
    :param date_from:
    :param date_to:
    :return:
    """
    hotels = await HotelDAO.get_available_by_loc_and_date(location, date_from, date_to)
    # TypeAdapter().validate_python() can ensure correct operation of redis
    # hotels_json = TypeAdapter(List[SHotel]).validate_python(hotels)
    return hotels


@router.get("id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SSingleHotel:
    hotel = await HotelDAO.find_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotAvailableException()
    return hotel
