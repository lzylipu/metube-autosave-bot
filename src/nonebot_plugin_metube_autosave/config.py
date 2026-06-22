from nonebot import get_plugin_config
from pydantic import BaseModel, Field


class Config(BaseModel):
    metube_endpoint: str = "http://metube:8081"
    simple_command: str | int = "1"
    progress_enabled: bool = True
    progress_interval_seconds: int = Field(default=5, ge=2)
    progress_timeout_seconds: int = Field(default=1800, ge=30)


plugin_config: Config = get_plugin_config(Config)
