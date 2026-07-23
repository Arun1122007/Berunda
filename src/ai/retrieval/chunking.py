from __future__ import annotations

from typing import Any

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)


def create_text_splitter(
    strategy: str = "recursive",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    **kwargs,
) -> Any:
    """Factory for text splitters."""
    if strategy == "recursive":
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            **kwargs,
        )
    if strategy == "sentence":
        return SentenceTransformersTokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **kwargs,
        )
    raise ValueError(f"Unknown chunking strategy: {strategy}")


def chunk_text(
    text: str,
    strategy: str = "recursive",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """Simple function to chunk text."""
    splitter = create_text_splitter(strategy, chunk_size, chunk_overlap)
    return splitter.split_text(text)


def chunk_documents(
    documents: list[dict[str, Any]],
    strategy: str = "recursive",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    text_key: str = "text",
    metadata_keys: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Chunk a list of documents with metadata preservation."""
    splitter = create_text_splitter(strategy, chunk_size, chunk_overlap)
    results = []

    for doc in documents:
        text = doc.get(text_key, "")
        if not text:
            continue

        chunks = splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            metadata = {}
            if metadata_keys:
                for k in metadata_keys:
                    if k in doc:
                        metadata[k] = doc[k]
            metadata["chunk_index"] = i
            metadata["source_id"] = doc.get("id", "")
            results.append({"text": chunk, "metadata": metadata})

    return results
