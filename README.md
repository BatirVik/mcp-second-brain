# MCP Second Brain

Easy shareable knowledge base.

## Use cases

- You want your model to have access to the latest version of library docs without web search.

- You are a library owner and want to share a prebuilt Docker with docs data.

## How to use?

1. **Prepare text data** with Firecrawl, Docling, or similar web crawler, and save all into one folder `data/`.

2. **Create Dockerfile:**

```Dockerfile
FROM mcp-second-brain
# ENV CHUNK_SIZE = 50_000 # env pass this way  
COPY data ./data
RUN python index.py ./data
RUN rm -r ./data # optional
```

3. **Build docker:**

```bash
docker buildx build -t mcp-sb-example .
```

> After you build the Docker image, you can push it into the container registry to share.

4. **Run docker:**

```bash
docker run -p 8000:8000 mcp-sb-example
```

5. **Connect and use!**

## Connect

### Claude Desktop

```json
{
  "mcpServers": {
    "sb-example": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp"
      ]
  }
}
```

### Raycast

**Command**: `npx` 

**Args**: `mcp-remote http://localhost:8000/mcp` 
