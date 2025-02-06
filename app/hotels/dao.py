from datetime import date

from sqlalchemy import select, func, and_

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    # @classmethod
    # async def find_all(cls):
    #     pass

    @classmethod
    async def get_available(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Rooms.hotel_id, func.count(Bookings.id).label("booked_count"))
                .join(Bookings, Bookings.room_id == Rooms.id)
                .where(
                    and_(
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from,
                    )
                )
                .group_by(Rooms.hotel_id)
                .cte("booked_rooms")
            )

            query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_quantity,
                    Hotels.image_id,
                    (
                        Hotels.rooms_quantity
                        - func.coalesce(booked_rooms.c.booked_count, 0)
                    ).label("rooms_left"),
                )
                .outerjoin(booked_rooms, booked_rooms.c.hotel_id == Hotels.id)
                .where(
                    and_(
                        Hotels.location == location,
                        (
                            Hotels.rooms_quantity
                            - func.coalesce(booked_rooms.c.booked_count, 0)
                        )
                        > 0,
                    )
                )
            )

            result = await session.execute(query)
            hotels = result.mappings().all()

            return hotels
