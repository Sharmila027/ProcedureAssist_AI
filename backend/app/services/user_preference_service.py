from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_preference import UserPreference


class UserPreferenceService:

    async def get_language(
        self,
        user_id: int,
        db: AsyncSession
    ) -> str:

        result = await db.execute(
            select(UserPreference).where(
                UserPreference.user_id == user_id
            )
        )

        preference = result.scalar_one_or_none()

        if preference:
            return preference.preferred_language

        return "en"

    async def save_language(
        self,
        user_id: int,
        language: str,
        db: AsyncSession
    ):

        result = await db.execute(
            select(UserPreference).where(
                UserPreference.user_id == user_id
            )
        )

        preference = result.scalar_one_or_none()

        if preference:
            preference.preferred_language = language

        else:
            preference = UserPreference(
                user_id=user_id,
                preferred_language=language
            )

            db.add(preference)

        await db.commit()
        await db.refresh(preference)

        return preference