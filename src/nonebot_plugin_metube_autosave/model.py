from typing import Any

from pydantic import BaseModel, Field


class AddTaskPayload(BaseModel):
    url: str
    quality: str = "best"
    format: str | None = "any"
    folder: str | None = None
    custom_name_prefix: str | None = None
    playlist_strict_mode: bool | None = None
    playlist_item_limit: int | None = None
    auto_start: bool | None = True


class MeTubeResponse(BaseModel):
    status: str
    msg: str | None = None


class DownloadItem(BaseModel):
    id: str | None = None
    url: str | None = None
    title: str | None = None
    status: str | None = None
    progress: float | str | None = None
    percent: float | str | None = None
    filename: str | None = None
    error: str | None = None
    download_dir: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> "DownloadItem":
        known = {
            "id": raw.get("id"),
            "url": raw.get("url") or raw.get("id"),
            "title": raw.get("title"),
            "status": raw.get("status"),
            "progress": raw.get("progress"),
            "percent": raw.get("percent"),
            "filename": raw.get("filename") or raw.get("name"),
            "error": raw.get("error") or raw.get("msg"),
            "download_dir": raw.get("download_dir") or raw.get("folder"),
        }
        return cls(**known, extra=raw)

    def progress_text(self) -> str | None:
        for value in [self.percent, self.progress, self.extra.get("percent"), self.extra.get("progress")]:
            if value is None:
                continue
            if isinstance(value, (int, float)):
                if 0 <= float(value) <= 1:
                    return f"{float(value) * 100:.0f}%"
                return f"{float(value):.0f}%"
            text = str(value).strip()
            if text:
                return text
        downloaded = self.extra.get("downloaded_bytes")
        total = self.extra.get("total_bytes") or self.extra.get("total_bytes_estimate")
        if isinstance(downloaded, (int, float)) and isinstance(total, (int, float)) and total > 0:
            return f"{downloaded / total * 100:.0f}%"
        return None


class HistoryResponse(BaseModel):
    done: list[DownloadItem] = Field(default_factory=list)
    queue: list[DownloadItem] = Field(default_factory=list)
    pending: list[DownloadItem] = Field(default_factory=list)

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> "HistoryResponse":
        return cls(
            done=[DownloadItem.from_raw(item) for item in raw.get("done", [])],
            queue=[DownloadItem.from_raw(item) for item in raw.get("queue", [])],
            pending=[DownloadItem.from_raw(item) for item in raw.get("pending", [])],
        )

    def find_by_url(self, url: str) -> tuple[str, DownloadItem] | None:
        for bucket_name in ["queue", "pending", "done"]:
            bucket = getattr(self, bucket_name)
            for item in bucket:
                if item.url == url or item.id == url or item.extra.get("url") == url or item.extra.get("id") == url:
                    return bucket_name, item
        return None
