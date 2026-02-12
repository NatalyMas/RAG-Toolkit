# если все же что-то надо будет делать на этой стороне
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DocumentProcessor:
    @staticmethod
    def prepare_chunks_for_storage(chunks: List[str],
                                   metadata: Dict[str, Any]) -> List[Dict]:
        """Подготовить чанки для сохранения в векторную БД"""
        prepared = []
        for i, chunk in enumerate(chunks):
            prepared.append({
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })
        return prepared
