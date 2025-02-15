from datetime import date

from sqlalchemy import select, and_, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_available_by_hotel_id_and_date(
        cls, hotel_id: int, date_from: date, date_to: date
    ):
        booked_rooms_cte = (
            select(
                Bookings.room_id,
                func.count(Bookings.id).label("booked_count"),
            )
            .join(Rooms, Rooms.id == Bookings.room_id)
            .where(
                and_(
                    Rooms.hotel_id == hotel_id,
                    Bookings.date_from < date_to,
                    Bookings.date_to > date_from,
                )
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        available_rooms = (
            select(
                Rooms.__table__.columns,
                (Rooms.price * (date_to - date_from).days).label("total_cost"),
                (
                    Rooms.quantity
                    - func.coalesce(booked_rooms_cte.c.booked_count, 0)
                ).label("rooms_left"),
            )
            .outerjoin(booked_rooms_cte, booked_rooms_cte.c.room_id == Rooms.id)
            .where(
                and_(
                    Rooms.hotel_id == hotel_id,
                    (
                        Rooms.quantity
                        - func.coalesce(booked_rooms_cte.c.booked_count, 0)
                    )
                    > 0,
                )
            )
        )

        async with async_session_maker() as session:
            rooms_set = await session.execute(available_rooms)
            # mappings() can ensure correct operation of redis
            available_rooms = rooms_set.mappings().all()

        return available_rooms
