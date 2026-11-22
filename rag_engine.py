
import os
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


# Knowledge base directory
KNOWLEDGE_BASE_DIR = Path(__file__).parent / "data" / "knowledge_base"


# Local embedding model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents():

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if content.strip():
            documents.append({
                "source": file_path.name,
                "content": content
            })

    return documents


def split_documents(documents, chunk_size=500, overlap=100):

    chunks = []

    for document in documents:

        text = document["content"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "source": document["source"],
                    "content": chunk_text
                })

            start += chunk_size - overlap

    return chunks


def create_vector_store():

    documents = load_documents()

    if not documents:
        raise ValueError("No knowledge-base documents found.")

    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("No document chunks were generated.")

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])

    index.add(embeddings)

    return model, index, chunks


def retrieve_relevant_documents(
    question,
    model,
    index,
    chunks,
    top_k=3
):

    if not question.strip():
        return []

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    top_k = min(top_k, len(chunks))

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        results.append({
            "source": chunks[idx]["source"],
            "content": chunks[idx]["content"],
            "score": float(score)
        })

    return results
