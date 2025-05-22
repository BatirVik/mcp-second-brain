import sys

from src.config import config
from src.docs import DocumentLoader, OneChunkReader, OverlapChunkReader


def main():
    [dir] = sys.argv[1:]

    match config.CHUNK_MODE:
        case "split":
            chunker = OverlapChunkReader(
                config.CHUNK_SIZE,
                config.PREV_CHUNK_OVERLAP_SIZE,
            )
        case "file":
            chunker = OneChunkReader(config.CHUNK_SIZE)

    DocumentLoader(chunker).load_dir(dir)


if __name__ == "__main__":
    main()
