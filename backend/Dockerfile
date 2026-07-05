FROM python:3.14.4-slim

WORKDIR /backend

RUN pip install uv

COPY pyproject.toml uv.lock ./
# froze, para que no updatee
RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]
