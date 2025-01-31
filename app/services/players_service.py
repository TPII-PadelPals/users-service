from typing import Any
from uuid import UUID

from app.core.config import settings

from .base_service import BaseService


class PlayersService(BaseService):
    def __init__(self) -> None:
        """Init the service."""
        super().__init__()
        self.name = "players-service"
        self._set_base_url(
            True, settings.PLAYERS_SERVICE_HOST, settings.PLAYERS_SERVICE_PORT
        )
        if settings.PLAYERS_SERVICE_API_KEY:
            self.set_base_headers({"x-api-key": settings.PLAYERS_SERVICE_API_KEY})

    async def create_player(self, user_public_id: UUID, telegram_id: int) -> Any:
        """Create player using players service."""
        return await self.post(
            "/api/v1/players/",
            json={
                "user_public_id": str(user_public_id),
                "telegram_id": int(telegram_id),
            },
        )
