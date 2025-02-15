from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoom


router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"],
)


@router.get("/{hotel_id}/rooms")
@cache(expire=30)
async def get_available_rooms_by_hotel_id(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[SRoom]:
    """
    Returns a list of all rooms available at a given hotel on a given date
    Requires authorization: no.
    :param hotel_id:
    :param date_from:
    :param date_to:
    :return:
    """
    rooms = await RoomDAO.find_available_by_hotel_id_and_date(
        hotel_id, date_from, date_to
    )

    return rooms
