import logging
from typing import Any

import httpx
from httpx._types import QueryParamTypes, RequestData

from app.utilities.exceptions import ExternalServiceException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self) -> None:
        """Init the service."""
        self.base_url = ""
        self.base_headers: dict[str, str] = {}
        self.timeout = 5
        self.name = "base-service"
        self._set_base_url("localhost", 8000)

    def _set_base_url(
        self, is_https: bool = False, host: str = "localhost", port: int | None = None
    ) -> None:
        """Set the base URL for the service."""
        local_server = ["localhost", "127.0.0.1"]
        service_url = f"{host}:{port}" if port is not None else f"{host}"
        self.base_url = (
            f"http://{service_url}"
            if host in local_server or is_https
            else f"https://{service_url}"
        )

    def set_base_headers(self, headers: dict[str, str]) -> None:
        """Set base headers for all requests."""
        self.base_headers = headers

    def generate_url(self, endpoint: str) -> str:
        """Generate a full URL from an endpoint."""
        return f"{self.base_url}{endpoint}"

    async def get(
        self,
        endpoint: str,
        params: QueryParamTypes | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Send a GET request."""
        url = self.generate_url(endpoint)
        all_headers = {**self.base_headers, **(headers or {})}
        logger.info(f"GET request to {url}, params: {params}, headers: {all_headers}")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params, headers=all_headers)
        return await self._handle_response(response)

    async def post(
        self,
        endpoint: str,
        data: RequestData | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Send a POST request."""
        url = self.generate_url(endpoint)
        all_headers = {**self.base_headers, **(headers or {})}
        logger.info(
            f"POST request to {url}, data: {data}, json: {json}, headers: {all_headers}"
        )
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, data=data, json=json, headers=all_headers)
        return await self._handle_response(response)

    async def put(
        self,
        endpoint: str,
        data: RequestData | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Send a PUT request."""
        url = self.generate_url(endpoint)
        all_headers = {**self.base_headers, **(headers or {})}
        logger.info(
            f"PUT request to {url}, data: {data}, json: {json}, headers: {all_headers}"
        )
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.put(url, data=data, json=json, headers=all_headers)
        return await self._handle_response(response)

    async def delete(self, endpoint: str, headers: dict[str, str] | None = None) -> Any:
        """Send a DELETE request."""
        url = self.generate_url(endpoint)
        all_headers = {**self.base_headers, **(headers or {})}
        logger.info(f"DELETE request to {url}, headers: {all_headers}")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(url, headers=all_headers)
        return await self._handle_response(response)

    async def _handle_response(self, response: httpx.Response) -> Any | None:
        """Handle the response, raise an exception for bad responses."""
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            try:
                logger.info(f"HTTP error: {e.response.json()}")
                raise ExternalServiceException(
                    self.name, e.response.json().get("detail")
                )
            except ValueError:
                logger.info(f"HTTP value error: {e.response.text}")
                raise ExternalServiceException(self.name, e.response.text)

        except Exception as e:
            logger.info(f"Error: {e}")
            raise ExternalServiceException(self.name, str(e))
