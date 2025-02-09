from contextlib import asynccontextmanager

from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.utilities.exceptions import ExternalServiceException


@asynccontextmanager
async def service_and_repository_error_handler(db: AsyncSession):
    """
    Async context manager to handle API and DB errors.
    """
    try:
        await db.begin()
        yield
        await db.commit()

    except ExternalServiceException as e:
        await db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except HTTPException as e:
        await db.rollback()
        raise e

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
