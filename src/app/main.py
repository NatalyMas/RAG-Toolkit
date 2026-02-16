from fastapi import FastAPI
from src.app.api.endpoints import api_functions

app = FastAPI(
    title="RAG Service",
    description="RAG-сервис с заменяемыми компонентами",
    version="0.1.0"
)

app.include_router(api_functions.router, tags=["functions"])
