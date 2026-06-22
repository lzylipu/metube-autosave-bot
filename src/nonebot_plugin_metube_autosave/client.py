from typing import Any

import httpx

from .config import plugin_config
from .exception import MeTubeException
from .model import AddTaskPayload, HistoryResponse, MeTubeResponse


class MeTubeClient:
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            base_url=plugin_config.metube_endpoint.rstrip("/"),
            timeout=httpx.Timeout(20.0, connect=10.0),
        )
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()

    async def add_task(self, payload: AddTaskPayload) -> MeTubeResponse:
        response = await self.client.post("/add", json=payload.model_dump())
        response.raise_for_status()
        data = response.json()
        result = MeTubeResponse(**data)
        if result.status != "ok":
            raise MeTubeException(result.msg or "add task failed")
        return result

    async def get_history(self) -> HistoryResponse:
        response = await self.client.get("/history")
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return HistoryResponse.from_raw(data)
