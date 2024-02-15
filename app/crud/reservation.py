from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from app.crud.base import CRUDBase
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):

    @staticmethod
    async def get_reservations_at_the_same_time(
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )

        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )

        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    @staticmethod
    async def get_future_reservations_for_room(
            room_id: int,
            session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )

        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)