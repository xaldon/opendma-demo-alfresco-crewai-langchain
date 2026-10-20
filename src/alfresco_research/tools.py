from __future__ import annotations

from crewai.tools import BaseTool
from crewai.tools.base_tool import Tool
from langchain_opendma import AlfrescoToolkit
from langchain_opendma.content_handlers import DoclingLoaderContentHandler

from alfresco_research.settings import Settings, load_settings


def create_alfresco_tools(settings: Settings | None = None) -> list[BaseTool]:
    settings = settings or load_settings()
    toolkit = AlfrescoToolkit(
        endpoint=settings.opendma_alfresco_endpoint,
        username=settings.opendma_alfresco_username,
        password=settings.opendma_alfresco_password,
        repository_id=settings.opendma_alfresco_repository_id,
        content_handlers=[DoclingLoaderContentHandler()],
    )
    return [Tool.from_langchain(tool) for tool in toolkit.get_tools()]


def create_alfresco_tools_by_name(settings: Settings | None = None) -> dict[str, BaseTool]:
    return {tool.name: tool for tool in create_alfresco_tools(settings)}
