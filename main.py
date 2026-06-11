import os
from src.promptService import OllamaService
from src.dbService import QdrantService
from src.embeddingService import EmbeddingService
from src.ingestService import IngestService

COLLECTION_NAME = "wiki_pages"

def ingest():
    qdrant = QdrantService(host="localhost", port=6333)
    embedder = EmbeddingService()
    ingester = IngestService(qdrant, embedder)

    pages_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "confluence_pages")
    ingester.ingest(pages_dir, COLLECTION_NAME)

def query(question: str):
    qdrant = QdrantService(host="localhost", port=6333)
    embedder = EmbeddingService()
    ollama = OllamaService()

    query_vector = embedder.embed([question])[0]

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=3
    )

    context = [r["payload"]["text"] for r in results]

    answer = ollama.ask(context, question)

    print("\nFinal Answer:\n")
    print(answer)

def main():
    #ingest()
    query("What is the formula for Periodic Fee Calculation?")


if __name__ == "__main__":
    main()