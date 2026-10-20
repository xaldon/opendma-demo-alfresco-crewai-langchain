from __future__ import annotations

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from alfresco_research.settings import load_settings
from alfresco_research.tools import create_alfresco_tools


@CrewBase
class AlfrescoResearchCrew:
    """CrewAI crew that researches documents stored in Alfresco."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def repository_researcher(self) -> Agent:
        settings = load_settings()
        return Agent(
            config=self.agents_config["repository_researcher"],
            tools=create_alfresco_tools(settings),
            llm=settings.crewai_model,
            verbose=True,
        )

    @agent
    def project_risk_analyst(self) -> Agent:
        settings = load_settings()
        return Agent(
            config=self.agents_config["project_risk_analyst"],
            llm=settings.crewai_model,
            verbose=True,
        )

    @task
    def research_project_documents(self) -> Task:
        return Task(config=self.tasks_config["research_project_documents"])

    @task
    def rank_project_risks(self) -> Task:
        return Task(config=self.tasks_config["rank_project_risks"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

