from datetime import date

from fastapi import APIRouter

from app.exceptions import HotelNotAvailableException
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SSingleHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}")
async def get_available_hotels(
    location: str,
    date_from: date,
    date_to: date,
) -> list[SHotel]:
    """
    Returns a list of hotels, must have at least 1 free room.
    Requires authorization: no.
    :param location:
    :param date_from:
    :param date_to:
    :return:
    """
    hotels = await HotelDAO.get_available(location, date_from, date_to)
    return hotels


@router.get("id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SSingleHotel:
    hotel = await HotelDAO.find_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotAvailableException()
    return hotel
