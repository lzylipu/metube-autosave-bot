from typing import Any

import httpx
from nonebot import logger

from .config import plugin_config
from .exception import MeTubeException
from .model import AddTaskPayload, HistoryResponse, MeTubeResponse

REQUEST_TIMEOUT = httpx.Timeout(20.0, connect=10.0)
MAX_RETRIES = 2


class MeTubeClient:
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            base_url=plugin_config.metube_endpoint.rstrip("/"),
            timeout=REQUEST_TIMEOUT,
        )
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def _request_with_retry(self, method: str, url: str, **kwargs) -> httpx.Response:
        """带重试的请求，处理瞬态错误"""
        last_error = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                return await self.client.request(method, url, **kwargs)
            except (httpx.ConnectError, httpx.ReadTimeout) as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    logger.warning(f"Request failed (attempt {attempt+1}/{MAX_RETRIES+1}): {url}")
                    import asyncio
                    await asyncio.sleep(1.0 * (attempt + 1))
        raise MeTubeException(f"请求失败（重试{MAX_RETRIES}次）: {last_error}")

    async def add_task(self, payload: AddTaskPayload) -> MeTubeResponse:
        response = await self._request_with_retry("POST", "/add", json=payload.model_dump())
        response.raise_for_status()
        result = MeTubeResponse(**response.json())
        if result.status != "ok":
            raise MeTubeException(result.msg or "add task failed")
        return result

    async def get_history(self) -> HistoryResponse:
        response = await self._request_with_retry("GET", "/history")
        response.raise_for_status()
        return HistoryResponse.from_raw(response.json())
