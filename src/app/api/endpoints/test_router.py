from fastapi import APIRouter
from ...services.custom_rag.embedding_client import EmbeddingClient
from ...services.custom_rag.vector_client import VectorClient
from ...core.config import settings

test_router = APIRouter(prefix="/test", tags=["test"])


@test_router.get("/embedding")
async def test_embedding():
    """Тест подключения к эмбеддинг-сервису"""
    try:
        url = settings.EMBEDDING_URL
        client = EmbeddingClient(base_url=url)
        test_text = "Тестовый текст для проверки эмбеддинга"
        embedding = client.get_embedding(test_text)
        return {
            "status": "success",
            "embedding_service": url,
            "embedding_length": len(embedding),
            "first_5_values": embedding[:5]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@test_router.get("/qdrant")
async def test_qdrant():
    """Тест подключения к Qdrant"""
    try:
        client = VectorClient(
            url=f"{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
        )
        connected = client.test_connection()

        return {
            "status": "success" if connected else "error",
            "qdrant_url": f"{settings.QDRANT_HOST}:{settings.QDRANT_PORT}",
            "connected": connected
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@test_router.get("/config")
async def test_config():
    """Показать текущую конфигурацию"""
    return {
        "embedding_url": settings.EMBEDDING_URL,
        "qdrant_host": settings.QDRANT_HOST,
        "qdrant_port": settings.QDRANT_PORT,
        "collection_name": settings.COLLECTION_NAME
    }


@test_router.get("/collections")
async def test_collections():
    """Показать все коллекции в Qdrant"""
    try:
        client = VectorClient(
            url=f"{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
        )
        collections = client.get_collections()
        return {
            "status": "success",
            "collections": collections,
            "total": len(collections)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@test_router.get("/embedding-dimension")
async def test_embedding_dimension():
    """Узнать размерность эмбеддингов"""
    try:
        client = EmbeddingClient(base_url=settings.EMBEDDING_URL)
        test_text = "test"
        embedding = client.get_embedding(test_text)
        return {
            "status": "success",
            "dimension": len(embedding),
            "note": "Используй это значение в vector_size при создании коллекции"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
# @router.get("/llm")
# async def test_llm():
#     """Тест подключения к LLM"""
#     try:
#         executor = FunctionExecutor()
#
#         test_prompt = "расскажи анек категории б"
#         response = executor.llm_client.generate(test_prompt, max_tokens=20)
#
#         return {
#             "status": "success",
#             "llm_url": FunctionExecutor.LLM_URL,
#             "response": response,
#             "response_length": len(response)
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e)
#         }
