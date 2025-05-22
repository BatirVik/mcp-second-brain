import sys
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

TEST = "pytest" in sys.modules
ENV_FILENAME = ".env.test" if TEST else ".env"
ENV_PATH = Path(__file__).parent.parent / ENV_FILENAME


class Config(BaseSettings):
    CHUNK_MODE: Literal["split", "file"] = "split"

    CHUNK_SIZE: int = 50_000
    PREV_CHUNK_OVERLAP_SIZE: int = 500

    DOCS_SEARCH_N_RESULTS: int = 5

    model_config = SettingsConfigDict(env_file=ENV_PATH)


config = Config()  # type: ignore
