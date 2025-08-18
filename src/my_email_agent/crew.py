from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from composio import Composio  # Use the main Composio client

@CrewBase
class MyEmailAgentCrew():
    """MyEmailAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self) -> None:
        self.composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))  # Initialize Composio client
        self.tools = self.composio.tools.get(
            user_id=os.getenv("USER_EMAIL"),
            tools=["GMAIL_FETCH_MESSAGE_BY_THREAD_ID", "GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID", "GMAIL_LIST_THREADS", "GMAIL_FETCH_EMAILS"]
        )

    @agent
    def email_retriever(self) -> Agent:
        return Agent(
            config=self.agents_config['email_retriever'],
            tools=self.tools,  # Use pre-fetched tools
            verbose=True
        )

    @task
    def retrieve_context_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieve_context_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MyEmailAgent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )