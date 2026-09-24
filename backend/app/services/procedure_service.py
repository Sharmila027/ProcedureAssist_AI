from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.procedure import Procedure


class ProcedureService:

    async def get_by_code(
        self,
        code: str,
        db: AsyncSession
    ):
        result = await db.execute(
            select(Procedure).where(
                Procedure.code == code
            )
        )

        return result.scalar_one_or_none()