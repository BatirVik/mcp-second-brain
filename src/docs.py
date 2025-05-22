import sys
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path
from uuid import uuid4

from chromadb import PersistentClient
from loguru import logger

from src.file_utils import get_dir_files_recursive
from src.types import ChunkReader, Readable, StrPath

CHROMA_PATH = Path(__file__).parent.parent / ".chroma"


chroma_client = PersistentClient(str(CHROMA_PATH))
collection = chroma_client.get_or_create_collection("chunks")


def search_relevant_docs(query: str, limit: int) -> list[str]:
    res = collection.query(query_texts=query, n_results=limit, include=["documents"])
    [docs] = res["documents"]  # type: ignore
    return docs


class DocumentLoader:
    def __init__(self, chunker: ChunkReader) -> None:
        self.chunker = chunker

    def load_dir(self, dir: StrPath, *, max_workers: int = 5) -> None:
        files = get_dir_files_recursive(dir)
        with ThreadPoolExecutor(max_workers) as executor:
            futures = [executor.submit(self._add, file) for file in files]
            _, not_done = wait(futures)
            for future in not_done:
                if future.exception():
                    sys.exit(1)

    def _add(self, file: StrPath) -> None:
        try:
            docs: list[str] = []
            ids: list[str] = []

            with open(file) as fp:
                for chunk in self.chunker(fp):
                    docs.append(chunk)
                    ids.append(str(uuid4()))

            collection.add(ids=ids, documents=docs)
            logger.info("Added {f} (docs={d})", f=file, d=len(docs))
        except Exception:
            logger.exception("Failed to add {f}", f=file)


class ChunkSizeExceeded(Exception):
    pass


class OneChunkReader:
    def __init__(self, chunk_size: int) -> None:
        self.chunk_size = chunk_size

    def __call__(self, fp: Readable) -> Generator[str]:
        chunk = fp.read(self.chunk_size)
        if fp.read(1):
            raise ChunkSizeExceeded(self.chunk_size)
        yield chunk


class OverlapChunkReader:
    def __init__(self, chunk_size: int, prev_chunk_overlap_size: int):
        self.chunk_size = chunk_size
        self.prev_chunk_overlap_size = prev_chunk_overlap_size

    def __call__(self, fp: Readable) -> Generator[str]:
        prev_chunk_end = ""
        while True:
            chunk = fp.read(self.chunk_size)
            if not chunk:
                return
            yield prev_chunk_end + chunk
            prev_chunk_end = chunk[-self.prev_chunk_overlap_size :]
