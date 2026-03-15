import os
from crewai import Agent, LLM
from crewai.tools import tool
from crewai_tools import FileWriterTool
# Мы используем LLM из crewai, так что ChatOllama можно не импортировать здесь

# Инструменты
from langchain_community.tools import DuckDuckGoSearchRun
ddg_run = DuckDuckGoSearchRun()

@tool("internet_search")
def search_tool(query: str):
    """Полезно для поиска актуальной информации в интернете."""
    return ddg_run.run(query)

file_writer_tool = FileWriterTool()

class ContentCrewAgents:
    def __init__(self):
        # 1. ОБЯЗАТЕЛЬНО добавляем self. перед названием
        # 2. ОБЯЗАТЕЛЬНО добавляем ollama/ перед названием модели
        self.local_llm = LLM(
            model="ollama/llama3.1:latest", 
            base_url="http://127.0.0.1:11434"
        )

    def researcher_agent(self):
        return Agent(
            role='Аналитик-исследователь',
            goal='Найти 5 ключевых фактов по теме: {topic}',
            backstory="Вы профессиональный исследователь.Получив данные, СРАЗУ делай выводы.",
            tools=[search_tool],
            llm=self.local_llm,    # Добавили self.
            verbose=True,
            max_iter=3,           # Агент остановится после 3-й попытки
            allow_delegation=False # Чтобы он не перекидывал задачу другим, пока не закончит
        )

    def writer_agent(self):
        return Agent(
            role='Автор контента',
            goal='Написать статью на тему: {topic}',
            backstory="Вы технический писатель.",
            llm=self.local_llm,    # Добавили self.
            verbose=True,
            max_iter=3
        )

    def fact_checker_agent(self):
        return Agent(
            role='Специалист по проверке фактов',
            goal='Исправить ошибки в статье по теме {topic}',
            backstory="Вы дотошный редактор.",
            tools=[search_tool],
            llm=self.local_llm,    # Добавили self.
            verbose=True,
            max_iter=3
        )

    def editor_agent(self):
        return Agent(
            role='Главный редактор',
            goal='Сохранить финальную версию статьи.',
            backstory="Вы следите за качеством.",
            tools=[file_writer_tool],
            llm=self.local_llm,    # Добавили self.
            verbose=True,
            max_iter=3
        )