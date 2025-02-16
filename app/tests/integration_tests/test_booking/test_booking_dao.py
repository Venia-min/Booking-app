import pytest
from datetime import datetime

from sqlalchemy import select

from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.exceptions import UserIsNotOwnerException


@pytest.mark.asyncio
async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=1,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 1
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


@pytest.mark.asyncio
async def test_find_all_with_room_info(session):
    """Test retrieving all bookings with room info for a specific user."""
    user_id = 2  # Using existing user_id
    expected_booking = {
        "room_id": 1,
        "user_id": user_id,
        "date_from": datetime.strptime("2023-06-05", "%Y-%m-%d"),
        "date_to": datetime.strptime("2023-06-25", "%Y-%m-%d"),
        "price": 24500,
    }

    # Fetch bookings for the user with room information
    bookings = await BookingDAO.find_all_with_room_info(user_id)

    assert len(bookings) == 1  # User 2 has one booking
    assert bookings[0]["user_id"] == user_id
    assert bookings[0]["name"] == "Улучшенный с террасой и видом на озеро"
    assert bookings[0]["price"] == expected_booking["price"]
    assert "image_id" in bookings[0]
    assert "description" in bookings[0]


@pytest.mark.asyncio
async def test_delete_booking_success(session):
    """Test successful deletion of a booking by its owner."""
    user_id = 1
    booking_id = 1  # Booking exists in the database

    # Delete the booking
    deleted = await BookingDAO.delete(booking_id, user_id)

    assert deleted is True

    # Verify deletion
    result = await session.execute(
        select(Bookings).where(Bookings.id == booking_id)
    )
    booking = result.scalars().first()

    assert booking is None  # Booking should be deleted


@pytest.mark.asyncio
async def test_delete_booking_not_found():
    """Test deleting a non-existent booking returns False."""
    deleted = await BookingDAO.delete(9999, 1)  # Non-existent booking ID
    assert deleted is False


@pytest.mark.asyncio
async def test_delete_booking_not_owner():
    """Test deleting a booking when the user is not the owner."""
    user_id = 2  # Other user
    booking_id = 2  # Booking exists but belongs to user_id 1

    with pytest.raises(UserIsNotOwnerException):
        await BookingDAO.delete(booking_id, user_id)
