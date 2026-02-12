import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class LLMClient:
    """Клиент для LLM API с Bearer аутентификацией"""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 60):
        """
        Args:
            base_url: URL LLM API (например, "https://gpt-dev.com")
            api_key: Bearer токен для авторизации
            timeout: Таймаут запроса в секундах
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

        logger.info(f"LLMClient инициализирован для {base_url}")

    def generate(self, prompt: str, max_tokens: int = 300, **kwargs) -> str:
        """
        Простая генерация по промпту

        Args:
            prompt: Текст промпта
            max_tokens: Максимальное количество токенов

        Returns:
            Сгенерированный текст
        """

        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            **kwargs
        }

        return self._make_request(payload)

    def generate_with_context(self, question: str, context: str,
                              max_tokens: int = 500, **kwargs) -> str:
        """
        Генерация с контекстом (для RAG)

        Args:
            question: Вопрос пользователя
            context: Контекст из векторной базы
            max_tokens: Максимальное количество токенов

        Returns:
            Ответ с использованием контекста
        """
        prompt = f"""Используй предоставленный контекст для ответа на вопрос.

Контекст:
{context}

Вопрос: {question}

Ответ:"""

        return self.generate(prompt, max_tokens=max_tokens, **kwargs)

    def chat_completion(self, messages: list, **kwargs) -> str:
        """
        Chat completion формат (как у OpenAI)

        Args:
            messages: Список сообщений в формате [{"role": "user", "content": "..."}]

        Returns:
            Ответ модели
        """
        payload = {
            "messages": messages,
            **kwargs
        }

        return self._make_request(payload, endpoint="/v1/chat/completions")

    def _make_request(self, payload: Dict[str, Any], endpoint: str = "/v1/completions") -> str:
        """
        Базовый метод для отправки запроса

        Args:
            payload: Данные для отправки
            endpoint: Endpoint API

        Returns:
            Текст ответа
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()

            if "choices" in data:
                if len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "message" in choice:
                        return choice["message"]["content"]
                    elif "text" in choice:
                        return choice["text"]

            elif "text" in data:
                return data["text"]

            elif "response" in data:
                return data["response"]

            else:
                return str(data)

        except requests.exceptions.RequestException as e:
            logger.error(f"LLM API error: {e}")
            raise Exception(f"LLM service error: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"LLM response parsing error: {e}")
            raise Exception(f"Invalid LLM response: {str(e)}")

    def test_connection(self) -> bool:
        """Проверить подключение к LLM API"""
        try:
            response = self.generate("test", max_tokens=5)
            return True
        except:
            return False
