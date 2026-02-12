import requests
import logging
from typing import List

logger = logging.getLogger(__name__)


class EmbeddingClient:
    """Клиент для сервиса эмбеддингов"""

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Args:
            base_url: URL сервиса эмбеддингов (например, "http://gpt-dev.com:8000")
            timeout: Таймаут запроса в секундах
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def get_embedding(self, text: str) -> List[float]:
        """
        Получить эмбеддинг для текста
        Args:
            text: Текст для векторизации
        Returns:
            Список чисел (эмбеддинг)
        """
        return self.get_embeddings([text])[0]

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Получить эмбеддинги для списка текстов

        Args:
            texts: Список текстов для векторизации

        Returns:
            Список эмбеддингов
        """
        if not texts:
            return []

        url = f"{self.base_url}/v1/embeddings"
        payload = {
            "input": texts
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()

            embeddings = []
            for item in data.get("data", []):
                if "embedding" in item:
                    embeddings.append(item["embedding"])

            if len(embeddings) != len(texts):
                logger.warning(
                    f"Количество эмбеддингов ({len(embeddings)}) "
                    f"не совпадает с количеством текстов ({len(texts)})"
                )

            return embeddings

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе эмбеддингов: {e}")
            raise Exception(f"Embedding service error: {str(e)}")
        except (KeyError, ValueError) as e:
            logger.error(f"Ошибка парсинга ответа от эмбеддинг-сервиса: {e}")
            raise Exception(f"Invalid response from embedding service: {str(e)}")

    def test_connection(self) -> bool:
        """Проверить подключение к сервису"""
        try:
            url = f"{self.base_url}/v1/embeddings"
            response = requests.post(
                url,
                json={"input": ["test"]},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
