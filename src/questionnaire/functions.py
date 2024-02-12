from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.questionnaire.models import Survey
from src.questionnaire.schemas import SurveyBaseSchema


async def get_survey_questions(session: AsyncSession):
    async with session as async_session:
        query = select(Survey)
        surveys = await async_session.execute(query)
        return [SurveyBaseSchema(id=survey.id, category=survey.category) for survey in surveys.scalars().all()]