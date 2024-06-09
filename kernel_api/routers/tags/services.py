from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import Tags

async def get_all_tags(db_session: AsyncSession):
    result = await db_session.execute(select(Tags))
    tags = result.scalar_one_or_none()
        
    if tags:
        return {
            "partnersItems": tags.partners_items,
            "educationItems": tags.education_items,
            "organizationItems": tags.organization_items
        }
    else:
        return {
            "partnersItems": [],
            "educationItems": [],
            "organizationItems": []
        }