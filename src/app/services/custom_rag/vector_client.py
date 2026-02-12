import json
import logging
import time
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue
)

logger = logging.getLogger(__name__)


class VectorClient:
    def __init__(self, url: str, timeout: int = 30):
        """
        Args:
            url: URL до Qdrant (http://host:port)
            timeout: в секундах
        """
        self.client = QdrantClient(url=url, timeout=timeout)
        logger.info(f"Qdrant client connected to {url}")

    def create_collection(self, collection_name: str, vector_size: int = 1024):
        """Создать коллекцию (если не существует)"""
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        logger.info(f"Collection '{collection_name}' created")
        return True

    def upsert_points(self, collection_name: str, vector: List[float],
                      payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Добавить точку в коллекции
        """

        point_id = int(time.time() * 1000)
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        )

        operation_info = self.client.upsert(
            collection_name=collection_name,
            points=[point]
        )

        logger.info(f"Added point {point_id} to collection '{collection_name}'")

        return {
            "point_id": point_id,
        }

    def search_points(self, collection_name: str, query_vector: List[float],
                      limit: int = 5, score_threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Поиск похожих векторов

        Args:
            collection_name: Имя коллекции
            query_vector: Вектор запроса
            limit: Количество результатов
            score_threshold: Минимальный скор (0-1)

        Returns:
            Список найденных точек с payload и score
        """
        search_result = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            with_vectors=True
        )

        results = []
        for hit in search_result:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
                # "vector": hit.vector if hasattr(hit, 'vector') else None,
                # **vars(hit)  # я хз надо это все или нет
            })

        return results

    def search_by_metadata(self, collection_name: str,
                           metadata_filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Поиск точек по метаданным
        Args:
            collection_name: Имя коллекции
            metadata_filters: Словарь {поле: значение} для фильтрации
        Returns:
            Список точек, соответствующих всем фильтрам
        """
        if not metadata_filters:
            return []

        must_conditions = []
        for key, value in metadata_filters.items():
            condition = FieldCondition(
                key=key,
                match=MatchValue(value=str(value))
            )
            must_conditions.append(condition)

        filter_condition = Filter(must=must_conditions)

        scroll_result = self.client.scroll(
            collection_name=collection_name,
            scroll_filter=filter_condition,
            # limit=limit,
            with_payload=True,
            with_vectors=False
        )
        results = []
        for point in scroll_result[0]:
            results.append({
                "id": point.id,
                "payload": point.payload,
            })

        return results

    def delete_point_by_id(self, collection_name: str, point_id: int):
        """Удалить конкретную точку по ID"""
        self.client.delete(
            collection_name=collection_name,
            points_selector=[point_id]
        )

    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Получить информацию о коллекции"""
        print("db")
        detailed_collection = self.client.get_collection(collection_name)
        collection_info = {
            "id": collection_name,
            "vectors_count": detailed_collection.points_count,
            "vector_size": detailed_collection.config.params.vectors.size,
            "status": str(detailed_collection.status),
        }
        return collection_info

    def delete_points(self, collection_name: str, point_ids: List[int]) -> Dict[str, Any]:
        """Удалить точки по ID"""
        try:
            operation_info = self.client.delete(
                collection_name=collection_name,
                points_selector=point_ids
            )
            return {
                "status": "success",
                "operation_id": operation_info.operation_id,
                "points_deleted": len(point_ids)
            }
        except Exception as e:
            logger.error(f"Error deleting points: {e}")
            raise

    def test_connection(self) -> bool:
        """Проверить подключение к Qdrant"""
        try:
            collections = self.client.get_collections()
            return True
        except:
            return False

    def get_collections(self) -> List[str]:
        """Получить список всех коллекций"""
        collections = self.client.get_collections()
        result = []
        for collection in collections.collections:
            result.append(str(collection.name))

        return result

    def delete_collection(self, collection_name: str) -> bool:
        """Удалить коллекцию"""
        collections = self.client.get_collections()
        exists = any(c.name == collection_name for c in collections.collections)

        if not exists:
            logger.warning(f"Collection '{collection_name}' does not exist")
            return False

        self.client.delete_collection(collection_name)
        logger.info(f"Collection '{collection_name}' deleted")
        return True

    def collection_exists(self, collection_name: str) -> bool:
        """Проверить существование коллекции"""
        collections = self.client.get_collections()
        return any(c.name == collection_name for c in collections.collections)
