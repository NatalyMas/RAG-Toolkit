import logging
import json
from typing import Dict, Any, List
from src.app.services.custom_rag.manager import CustomRAGManager
from src.app.services.custom_rag.validation_client import ValidationClient

logger = logging.getLogger(__name__)


class FunctionExecutor:
    """Центральный диспетчер функций для RAG сервиса"""

    def __init__(self):
        self.custom_rag_manager = CustomRAGManager()
        self.validator = ValidationClient()
        self.functions = self._build_catalog()

    def _build_catalog(self) -> Dict[str, Dict]:
        """Построить каталог доступных функций"""
        return {
            "add_to_database": {
                "id": "add_to_database",
                "name": "Добавить в базу знаний",
                "description": "Добавляет документ в векторную базу данных",
                "inputs": [
                    {
                        "title": "Текст документа",
                        "name": "text",
                        "type": "string"
                    },
                    {
                        "title": "Метаданные",
                        "name": "metadata",
                        "type": "array", "arrayType": "Map"
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ],
                "outputs": [
                    {
                        "title": "Добавить в базу знаний",
                        "name": "addition_result",
                        "type": "array", "arrayType": "Map"
                    }
                ],
                "controls": [
                    {
                        "title": "Текст документа",
                        "name": "text",
                        "type": "string"
                    },
                    {
                        "title": "Метаданные",
                        "name": "metadata",
                        "type": "array", "arrayType": "Map"
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ]
            },
            "search_documents": {
                "id": "search_documents",
                "name": "Поиск документов",
                "description": "Ищет документы по смыслу в векторной базе",
                "inputs": [
                    {
                        "title": "Запрос",
                        "name": "query",
                        "type": "string"
                    },
                    {
                        "title": "Порог схожести",
                        "name": "threshold",
                        "type": "number",
                        "optional": True
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ],
                "outputs": [
                        {
                            "title": "Найденные документы",
                            "name": "search_result",
                            "type": "array", "arrayType": "Map"
                        }
                    ],
                "controls": [
                    {
                        "title": "Запрос",
                        "name": "query",
                        "type": "string"
                    },
                    {
                        "title": "Порог схожести",
                        "name": "threshold",
                        "type": "number"
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ]
            },
            "search_by_payload": {
                "id": "search_by_payload",
                "name": "Поиск по метаданным",
                "description": "Ищет документы по параметрам в векторной базе",
                "inputs": [
                    {
                        "title": "Параметры",
                        "name": "params",
                        "type": "array", "arrayType": "Map"
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ],
                "outputs": [
                    {
                        "title": "Найденные документы",
                        "name": "search_result",
                        "type": "array", "arrayType": "Map"
                    }
                ],
                "controls": [
                    {
                        "title": "Параметры",
                        "name": "params",
                        "type": "array", "arrayType": "Map"
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ]
            },
            "delete_by_id": {
                "id": "delete_by_id",
                "name": "Удалить по id",
                "description": "Удаляет запись в коллекции по id",
                "inputs": [
                    {
                        "title": "Параметры",
                        "name": "params",
                        "type": "array", "arrayType": "Map"
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ],
                "outputs": [],
                "controls": [
                    {
                        "title": "Параметры",
                        "name": "params",
                        "type": "array", "arrayType": "Map"
                    },
                    {
                        "title": "Коллекция",
                        "name": "collection_name",
                        "type": "string"
                    }
                ]
            },
            "collections_list": {
                "id": "collections_list",
                "name": "Список коллекций",
                "description": "Показать все коллекции в Qdrant",
                "inputs": [],
                "outputs": [
                    {
                        "title": "Список коллекций",
                        "name": "collections_list",
                        "type": "array", "arrayType": "string"
                    }
                ],
                "controls": []
            },
            "create_collection": {
                "id": "create_collection",
                "name": "Создать коллекцию",
                "description": "Создать новую коллекцию в Qdrant",
                "inputs": [
                    {
                        "title": "Имя коллекции",
                        "name": "collection_name",
                        "type": "string"
                    }
                ],
                "outputs": [
                    {
                        "title": "Результат",
                        "name": "creation_result",
                        "type": "string"
                    }
                ],
                "controls": [
                    {
                        "title": "Имя коллекции",
                        "name": "collection_name",
                        "type": "string"
                    },
                ]
            },
            "delete_collection": {
                "id": "delete_collection",
                "name": "Удалить коллекцию",
                "description": "Удалить коллекцию из Qdrant",
                "inputs": [
                    {
                        "title": "Имя коллекции",
                        "name": "collection_name",
                        "type": "string"
                    }
                ],
                "outputs": [],
                "controls": [
                    {
                        "title": "Имя коллекции",
                        "name": "collection_name",
                        "type": "string"
                    }
                ]
            },
            "collection_info": {
                "id": "collection_info",
                "name": "Информация о коллекции",
                "description": "Информация о коллекции",
                "inputs": [
                    {
                        "title": "Имя коллекции",
                        "name": "collection_name",
                        "type": "string"
                    }
                ],
                "outputs": [
                    {
                        "title": "Результат",
                        "name": "collection_info",
                        "type": "Map"
                    }
                ],
                "controls": [
                    {
                        "title": "Имя коллекции",
                        "name": "collection_name",
                        "type": "string"
                    }
                ]
            },
            "validate_query": {
                "id": "validate_query",
                "name": "Проверить запрос",
                "description": "Проверяет запрос на соответствие критерию через LLM",
                "inputs": [
                    {
                        "title": "Запрос пользователя",
                        "name": "query",
                        "type": "string",
                        "optional": False
                    },
                    {
                        "title": "Оценочный вопрос",
                        "name": "question",
                        "type": "string",
                        "optional": False
                    }
                ],
                "outputs": [
                    {
                        "title": "Результат проверки",
                        "name": "validation_result",
                        "type": "Map"
                    }
                ],
                "controls": [
                    {
                        "title": "Запрос пользователя",
                        "name": "query",
                        "type": "string"
                    },
                    {
                        "title": "Оценочный вопрос",
                        "name": "question",
                        "type": "string"
                    }
                ]
            }

        }

    def get_catalog(self) -> str:
        """каталог функций"""
        catalog = [{
            "id": "rag",
            "title": "RAG Service",
            "functions": self.functions
        }]
        return json.dumps(catalog, ensure_ascii=False)

    def execute(self, function_id: str, parameters: Dict[str, Any]) -> Any:
        """выполнить функцию по ID"""
        logger.info(f"Executing function {function_id} with params: {parameters}")

        if function_id in ["list_collections"] and not parameters:
            parameters = {}

        function_map = {
            "add_to_database": self._execute_add_document,
            "search_documents": self._execute_search,
            "search_by_metadata" : self._execute_search_by_metadata,
            "delete_by_id": self._execute_delete_by_id,
            "collections_list": self._execute_list_collections,
            "create_collection": self._execute_create_collection,
            "delete_collection": self._execute_delete_collection,
            "collection_info": self._execute_collection_info,
            "validate_query": self._execute_validate_query
        }

        if function_id in function_map:
            print(f"выполняю функцию {function_id}")
            return function_map[function_id](parameters)
        else:
            raise ValueError(f"Unknown function: {function_id}")

    def _execute_add_document(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """добавить документ"""
        text = params.get("text")
        collection_name = params.get("collection_name")
        if not text:
            raise ValueError("Parameter 'text' is required")
        if not collection_name:
            raise ValueError("Parameter 'collection_name' is required")
        if not self.custom_rag_manager.vector_db.collection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' doesn't exist")
        metadata = params.get("metadata", {})
        result = self.custom_rag_manager.add_document(text, collection_name, metadata)
        return result

    def _execute_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """поиск документов"""
        query = params.get("query")
        collection_name = params.get("collection_name")
        if not query:
            raise ValueError("Parameter 'query' is required")
        if not collection_name:
            raise ValueError("Parameter 'collection_name' is required")
        if not self.custom_rag_manager.vector_db.collection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' doesn't exist")
        threshold = params.get("threshold", 0.8)

        result = self.custom_rag_manager.search(query, collection_name, threshold)
        return result

    def _execute_search_by_metadata(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Поиск по метаданным"""
        metadata_filters = params.get("metadata_filters", {})
        print(params)
        collection_name = params.get("collection_name")

        if not collection_name:
            raise ValueError("Parameter 'collection_name' is required")

        if not self.custom_rag_manager.vector_db.collection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' doesn't exist")

        if not metadata_filters:
            raise ValueError("Parameter 'metadata_filters' is required")

        result = self.custom_rag_manager.search_by_metadata(
            collection_name=collection_name,
            metadata_filters=metadata_filters
        )
        return result

    def _execute_delete_by_id(self, params: Dict[str, Any]) -> None:
        """Удалить документ по id"""
        point_id = params.get("id")
        collection_name = params.get("collection_name")

        if point_id is None:
            raise ValueError("Parameter 'point_id' is required")
        if not collection_name:
            raise ValueError("Parameter 'collection_name' is required")

        self.custom_rag_manager.delete_document(collection_name, point_id)

    def _execute_list_collections(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить получение списка коллекций"""
        result = self.custom_rag_manager.list_collections()
        return result

    def _execute_create_collection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Создать коллекцию"""
        collection_name = params.get("collection_name")
        if self.custom_rag_manager.vector_db.collection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' already exists")
        if not collection_name:
            raise ValueError("Parameter 'collection_name' is required")

        success = self.custom_rag_manager.vector_db.create_collection(
            collection_name=collection_name,
            vector_size=self.custom_rag_manager.embedding_dimension
        )

        return {
            "creation_result": collection_name
        }

    def _execute_delete_collection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Удалить коллекцию"""
        collection_name = params.get("collection_name")
        if not collection_name:
            raise ValueError("Parameter 'collection_name' is required")
        if not self.custom_rag_manager.vector_db.collection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' doesn't exist")

        success = self.custom_rag_manager.vector_db.delete_collection(collection_name)

    def _execute_collection_info(self, params: Dict[str, Any]):
        collection_name = params.get("collection_name")
        if not collection_name:
            raise ValueError("Parameter 'collection_name' is required")
        if not self.custom_rag_manager.vector_db.collection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' doesn't exist")
        result = self.custom_rag_manager.vector_db.get_collection_info(collection_name)
        return {"collection_info": result}

    def _execute_validate_query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Выполнить проверку запроса"""
        query = params.get("query")
        question = params.get("question")

        if not query:
            raise ValueError("Parameter 'query' is required")
        if not question:
            raise ValueError("Parameter 'question' is required")

        is_valid = self.validator.validate(query, question)

        return {"validation_result": {is_valid}}


function_executor = FunctionExecutor()
