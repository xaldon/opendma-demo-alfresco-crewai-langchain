from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    opendma_alfresco_endpoint: str
    opendma_alfresco_username: str
    opendma_alfresco_password: str
    opendma_alfresco_repository_id: str
    crewai_model: str


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        opendma_alfresco_endpoint=os.getenv(
            "OPENDMA_ALFRESCO_ENDPOINT",
            "http://localhost:7070/opendma/alf",
        ),
        opendma_alfresco_username=os.getenv("OPENDMA_ALFRESCO_USERNAME", "admin"),
        opendma_alfresco_password=os.getenv("OPENDMA_ALFRESCO_PASSWORD", "admin"),
        opendma_alfresco_repository_id=os.getenv("OPENDMA_ALFRESCO_REPOSITORY_ID", "Alfresco"),
        crewai_model=os.getenv("CREWAI_MODEL", "openai/gpt-4o-mini"),
    )

