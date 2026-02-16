import requests


class ValidationClient:
    """
    клиент для проверки запросов через компактную LLM
    перед отправкой в поиск контекста и большую LLM"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "mistral"

    def validate(self, query: str, question: str) -> bool:

        prompt = f"""Определи, относится ли запрос к указанной в вопросе теме.
        Ответь только одним словом: "да" или "нет".

        Примеры:
        Запрос: "Как установить драйвер?"
        Тема: "Запрос относится к IT разработке?"
        Ответ: да

        Запрос: "Сколько стоит хлеб?"
        Тема: "Запрос относится к IT разработке?"
        Ответ: нет

        Запрос: "Что такое бипки?"
        Тема: "Запрос относится к погодным условиям?"
        Ответ: нет

        Запрос: "{query}"
        Тема: "{question}"
        Ответ:"""

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 5
                    }
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip().lower()
            return result == "да" or result == "yes"

        except Exception as e:
            return False
