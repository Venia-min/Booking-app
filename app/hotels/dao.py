from datetime import date

from sqlalchemy import and_, func, select

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
    async def get_available_by_loc_and_date(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(
                    Rooms.hotel_id,
                    func.count(Bookings.id).label("booked_count"),
                )
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

            hotels_query = (
                select(
                    Hotels.__table__.columns,
                    (
                        Hotels.rooms_quantity
                        - func.coalesce(booked_rooms.c.booked_count, 0)
                    ).label("rooms_left"),
                )
                .outerjoin(booked_rooms, booked_rooms.c.hotel_id == Hotels.id)
                .where(
                    and_(
                        Hotels.location.ilike(f"%{location}%"),
                        (
                            Hotels.rooms_quantity
                            - func.coalesce(booked_rooms.c.booked_count, 0)
                        )
                        > 0,
                    )
                )
            )

            result = await session.execute(hotels_query)
            # mappings() can ensure correct operation of redis
            hotels = result.mappings().all()

            return hotels
