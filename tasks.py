from crewai import Task

class ContentCrewTasks:
    def research_task(self, agent, topic):
        return Task(
            description=f"Проведи глубокое исследование темы: {topic}. Найди 5 ключевых фактов и статистику.",
            # Изменили PDF на Markdown для удобства передачи между агентами
            expected_output="Структурированный Markdown-брифинг с фактами и ссылками на источники.",
            agent=agent
        )

    def write_task(self, agent, topic):
        return Task(
            description=f"Напиши статью в формате Markdown на тему: {topic}. Объем 800-1200 слов. Используй данные из исследования.",
            expected_output="Черновик статьи в формате Markdown с заголовками и выводами.",
            agent=agent
        )
    
    def fact_checking_task(self, agent, context_tasks):
        return Task(
            description="""Внимательно прочитайте черновик статьи. 
            Сверьте все ключевые факты и цифры с результатами исследования. 
            Исправьте любые неточности.""",
            expected_output="Скорректированный текст статьи, где все факты подтверждены.",
            agent=agent,
            context=context_tasks 
        )

    def edit_task(self, agent, topic):
        # Очищаем тему от пробелов для названия файла
        clean_topic = topic.replace(" ", "_").replace("/", "_")
        return Task(
            description="Проверь текст на ошибки, улучши стиль и сохрани финальную версию.",
            expected_output="Финальная отполированная статья в формате Markdown.",
            agent=agent,
            output_file=f'output/{clean_topic}.md' # Файл будет создан автоматически
        )