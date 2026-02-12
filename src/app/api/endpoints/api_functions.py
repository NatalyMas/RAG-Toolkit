from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json

from src.app.core.function_executor import function_executor
router = APIRouter()


@router.get("/functions")
async def get_available_functions():
    """возвращает каталог из FunctionExecutor"""
    catalog_json = function_executor.get_catalog()
    catalog = json.loads(catalog_json)
    # print(catalog[0]["functions"]["search_documents"])
    return catalog


@router.post("/functions/{function_id}")
async def execute_function(function_id: str, request_data: Dict[str, Any]):
    """вызывает execute по id"""
    parameters = request_data.get("parameters", {})

    try:
        result = function_executor.execute(function_id, parameters)
        print(f"функция {function_id} выполнена с результатом \n {result}")
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
