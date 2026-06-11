import os
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from src.embeddingService import EmbeddingService
from src.dbService import QdrantService

class IngestService:
	def __init__(self, db_service: QdrantService, embedding_service: EmbeddingService):
		self.db_service = db_service
		self.embedding_service = embedding_service

	def read_html_files(self, folder_path: str) -> List[Dict[str, str]]:
		documents = []
		for filename in os.listdir(folder_path):
			if not filename.endswith(".html"):
				continue
			filepath = os.path.join(folder_path, filename)
			with open(filepath, "r", encoding="utf-8") as f:
				html = f.read()
			soup = BeautifulSoup(html, "html.parser")
			title = soup.title.string if soup.title else filename
			text = soup.get_text(separator="\n", strip=True)
			if text:
				documents.append({"title": title, "text": text, "source": filename})
		return documents

	def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
		chunks = []
		start = 0
		while start < len(text):
			end = start + chunk_size
			chunks.append(text[start:end])
			start += chunk_size - overlap
		return chunks

	def ingest(self, folder_path: str, collection_name: str = "wiki_pages"):
		self.db_service.create_collection(collection_name)

		documents = self.read_html_files(folder_path)
		print(f"Read {len(documents)} HTML files from '{folder_path}'.")

		all_vectors = []
		all_payloads = []

		for doc in documents:
			chunks = self.chunk_text(doc["text"])
			vectors = self.embedding_service.embed(chunks)

			for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
				all_vectors.append(vector)
				all_payloads.append({
					"title": doc["title"],
					"source": doc["source"],
					"chunk_index": i,
					"text": chunk
				})

		if all_vectors:
			self.db_service.insert(collection_name, all_vectors, all_payloads)
			print(f"Ingested {len(all_vectors)} chunks into collection '{collection_name}'.")
		else:
			print("No content found to ingest.")
