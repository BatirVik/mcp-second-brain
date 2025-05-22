from chromadb.utils import embedding_functions

if __name__ == "__main__":
    embedding_functions.DefaultEmbeddingFunction()([""])  # downloads on first use
