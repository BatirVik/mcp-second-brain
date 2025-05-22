import tempfile

import pytest

from src.docs import ChunkSizeExceeded, OneChunkReader, OverlapChunkReader


def test_overlap_chunk_reader():
    chunk_reader = OverlapChunkReader(4, 2)

    with tempfile.TemporaryFile(mode="w+") as fp:
        fp.write("123456789")
        fp.seek(0)
        chunks = list(chunk_reader(fp))

    assert chunks == ["1234", "345678", "789"]


def test_one_chunk_reader():
    chunk_reader = OneChunkReader(4)

    with tempfile.TemporaryFile(mode="w+") as fp:
        fp.write("123")
        fp.seek(0)
        chunks = list(chunk_reader(fp))

    assert chunks == ["123"]

    with tempfile.TemporaryFile(mode="w+") as fp:
        fp.write("12345")
        fp.seek(0)
        with pytest.raises(ChunkSizeExceeded):
            list(chunk_reader(fp))
