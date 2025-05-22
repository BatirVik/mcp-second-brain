FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --no-group dev


FROM python:3.12-slim

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src/
COPY main.py index.py download_model.py ./

RUN python download_model.py

EXPOSE 8000

CMD ["python", "main.py"]


# FROM mcp-second-brain
# COPY data ./data
# RUN ./index.py ./data
# RUN rm -r ./data

