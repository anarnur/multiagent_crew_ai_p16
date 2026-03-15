import os
from dotenv import load_dotenv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Загружаем переменные из .env
load_dotenv()

os.environ["OPENAI_API_KEY"] = "NA"

# Настройки LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "CrewAI_Ollama_Debugging" # Название проекта в панели

from crew import ContentCrew

def main():
    topic = "Краткий обзор достижений квантовых вычислений к 2026 году"
    print(f"🚀 Запускаем локальную модель Ollama для темы: {topic}")
    
    try:
        crew_instance = ContentCrew(topic)
        result = crew_instance.run()
        print("\n--- ГОТОВО ---")
        print(result)
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    main()