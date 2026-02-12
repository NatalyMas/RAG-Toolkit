# import json
import logging
from typing import List, Dict, Any, Optional
from .embedding_client import EmbeddingClient
from .vector_client import VectorClient
from ...core.config import settings

logger = logging.getLogger(__name__)


class CustomRAGManager:
    def __init__(self):
        self.embedder = EmbeddingClient(base_url=settings.EMBEDDING_URL)
        self.vector_db = VectorClient(
            url=f"{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
        )
        self.embedding_dimension = self._get_embedding_dimension()
        logger.info(f"RAG manager initialized. Embedding dimension: {self.embedding_dimension}")

    def _get_embedding_dimension(self) -> int:
        """Определить размерность эмбеддингов"""
        try:
            test_text = "test"
            embedding = self.embedder.get_embedding(test_text)
            dimension = len(embedding)
            logger.info(f"Embedding dimension detected: {dimension}")
            return dimension
        except Exception as e:
            logger.error(f"Cannot detect embedding dimension: {e}")
            return 1024

    def add_document(self, text: str, collection_name: str,
                     metadata: Optional[Dict] = None,
                     ) -> Dict[str, Any]:
        """
        Добавить документ в базу знаний

        Args:
            text: Текст документа
            metadata: Дополнительные метаданные
            collection_name: Имя коллекции (обязательно)

        Returns:
            Словарь с результатом
        """
        embedding = self.embedder.get_embedding(text)

        if len(embedding) != self.embedding_dimension:
            logger.warning(
                f"Embedding dimension mismatch: "
                f"expected {self.embedding_dimension}, got {len(embedding)}"
            )

        payload = {"text": text}
        if metadata:
            try:
                if isinstance(metadata, dict):
                    payload.update(metadata)
                elif isinstance(metadata, str):
                    import json
                    metadata_dict = json.loads(metadata)
                    payload.update(metadata_dict)
                else:
                    logger.warning(f"Unexpected metadata type: {type(metadata)}")
            except Exception as meta_error:
                logger.warning(f"Could not process metadata: {meta_error}")
        result = self.vector_db.upsert_points(
            collection_name=collection_name,
            vector=embedding,
            payload=payload
        )
        results = {
                "addition_result": {
                    "id": result.get("point_id", "N/A"),
                    # "text": text,
                    "payload": payload,
                    # "collection_name": collection_name,
                    # "embedding_dimension": len(embedding),
                    # "embedding": embedding,
                }
            }
        # import os
        # import json
        # os.makedirs('src/app/services/files/', exist_ok=True)
        # with open("src/app/services/files/add_result.json", 'w', encoding='utf-8') as f:
        #     json.dump(results, f, ensure_ascii=False, indent=4, default=str)
        #     print(f"Сохранено в add_result.json")

        return results

    def search(self, query: str, collection_name: str, threshold: float = 0.8) \
            -> Dict[str, Any]:
        """Поиск в указанной коллекции"""

        if not collection_name or not isinstance(collection_name, str):
            return {}

        query_embedding = self.embedder.get_embedding(query)
        results = self.vector_db.search_points(
            collection_name=collection_name,
            query_vector=query_embedding,
            score_threshold=threshold
        )

        if not results:
            return {"search_result": []}
        else:
            # import os
            # os.makedirs('src/app/services/files/', exist_ok=True)
            # with open("src/app/services/files/search_result.json", 'w', encoding='utf-8') as f:
            #     json.dump(results, f, ensure_ascii=False, indent=4, default=str)
            #     print(f"Сохранено в search_result.json")
            return {"search_result": results}

    def search_by_metadata(self, collection_name: str,
                           metadata_filters: Dict[str, Any]) -> Dict[str, Any]:
        """Поиск документов по метаданным"""

        if not self.vector_db.collection_exists(collection_name):
            return {"search_by_metadata_result": []}

        if not metadata_filters:
            return {"search_by_metadata_result": []}

        clean_filters = {}
        for key, value in metadata_filters.items():
            if value is not None and value != "":
                clean_filters[key] = value

        if not clean_filters:
            return {"search_by_metadata_result": []}
        results = self.vector_db.search_by_metadata(
            collection_name=collection_name,
            metadata_filters=clean_filters
        )
        return {"search_by_metadata_result": results}

    def batch_add_documents(self, documents: List[str],
                            metadatas: Optional[List[Dict]] = None,
                            collection_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Пакетное добавление документов

        Args:
            documents: Список текстов
            metadatas: Список метаданных (опционально)
            collection_name: Имя коллекции

        Returns:
            Результат операции
        """
        target_collection = collection_name
        try:
            embeddings = self.embedder.get_embeddings(documents)

            for i, emb in enumerate(embeddings):
                if len(emb) != self.embedding_dimension:
                    logger.warning(
                        f"Document {i}: embedding dimension mismatch: "
                        f"expected {self.embedding_dimension}, got {len(emb)}"
                    )

            payloads = []
            for i, text in enumerate(documents):
                payload = {"text": text}
                if metadatas and i < len(metadatas):
                    payload.update(metadatas[i])
                payloads.append(payload)

            result = self.vector_db.upsert_points(
                collection_name=target_collection,
                vectors=embeddings,
                payloads=payloads
            )

            return {
                "status": "success",
                "message": f"Added {len(documents)} documents to '{target_collection}'",
                "collection": target_collection,
                "count": len(documents),
                "operation_id": result.get("operation_id")
            }

        except Exception as e:
            logger.error(f"Error in batch add: {e}")
            raise

    def delete_document(self, collection_name: str, point_id: int) -> None:
        """
        Удалить документ по ID точки
        Args:
            collection_name: Имя коллекции
            point_id: ID точки для удаления
        """
        self.vector_db.delete_point_by_id(
                collection_name=collection_name,
                point_id=point_id
            )

    def list_collections(self) -> dict[str, List]:
        """Получить список всех коллекций в виде дикшинари"""
        collections = self.vector_db.get_collections()
        if not collections:
            return {"collections_list": []}

        return {"collections_list": collections}
