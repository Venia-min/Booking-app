from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomCannotBeBookedException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[SBooking]:
    """
    Returns a list of all user bookings.
    Requires authorization: yes.
    :param user:
    :return:
    """
    response = await BookingDAO.find_all(user_id=user.id)
    return response


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    """
    Creates a reservation for the user if rooms are available.
    Requires authorization: yes.
    :param room_id:
    :param date_from:
    :param date_to:
    :param user:
    :return:
    """
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException()
    booking_dict = TypeAdapter(SBooking).validate_python(booking).dict()
    try:
        send_booking_confirmation_email.delay(booking_dict, user.email)
    finally:
        return booking_dict


@router.delete("/{booking_id}")
async def del_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    """
    Deletes a user booking.
    Requires authorization: yes.
    :param booking_id:
    :param user:
    :return:
    """
    await BookingDAO.delete(user.id, booking_id)
