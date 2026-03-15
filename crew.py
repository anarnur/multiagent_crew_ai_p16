from crewai import Crew, Process
from agents import ContentCrewAgents
from tasks import ContentCrewTasks

class ContentCrew:
    # Этот метод обязателен, чтобы принимать тему (topic)
    def __init__(self, topic):
        self.topic = topic

    def run(self):
        agents = ContentCrewAgents()
        tasks = ContentCrewTasks()

        # Создаем агентов
        researcher = agents.researcher_agent()
        writer = agents.writer_agent()
        fact_checker = agents.fact_checker_agent()
        editor = agents.editor_agent()

        # Создаем задачи, передавая self.topic
        t1 = tasks.research_task(researcher, self.topic)
        t2 = tasks.write_task(writer, self.topic)
        t3 = tasks.fact_checking_task(fact_checker, [t1, t2])
        t4 = tasks.edit_task(editor, self.topic)

        crew = Crew(
            agents=[researcher, writer, fact_checker, editor],
            tasks=[t1, t2, t3, t4],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()