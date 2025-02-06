from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.schemas import SRoom

router = APIRouter(
    prefix="/hotels",
    tags=["Rooms"],
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date,
) -> list[SRoom]:
    """
    Returns a list of all rooms in a given hotel.
    Requires authorization: no.
    :param hotel_id:
    :param date_from:
    :param date_to:
    :return:
    """

    pass
