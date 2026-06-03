from ollama_service import OllamaService
from qdrant_service import QdrantService

def main():
    qdrant = QdrantService(host="localhost", port=6333)
    ollama = OllamaService()

    query = "What is an assignment?"

    results = qdrant.search(
        collection_name="pdf_docs",
        query_vector=[0.1, 0.2, 0.3],  # replace with real embedding
        limit=3
    )

    context = [r["payload"]["text"] for r in results]

    answer = ollama.ask(context, query)

    print("\nFinal Answer:\n")
    print(answer)


if __name__ == "__main__":
    main()