from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct
)
from typing import List, Dict, Any
import uuid

class QdrantService:
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host=host, port=port)

    def create_collection(self, collection_name: str, vector_size: int = 384):
        if collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")

    def insert(
        self,
        collection_name: str,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]]
    ):
        points = []
        for vector, payload in zip(vectors, payloads):
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

        print(f"Inserted {len(points)} points.")

    def update(
        self,
        collection_name: str,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]]
    ):
        points = []
        for pid, vector, payload in zip(ids, vectors, payloads):
            points.append(
                PointStruct(
                    id=pid,
                    vector=vector,
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

        print(f"Updated {len(points)} points.")

    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5
    ):
        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )

        output = []
        for r in results:
            output.append({
                "id": r.id,
                "score": r.score,
                "payload": r.payload
            })

        return output