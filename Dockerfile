FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock .

RUN pip3 install poetry && poetry install

COPY . .

EXPOSE 8080

CMD ["poetry", "run", "streamlit", "run", "programmer_gpt/main.py"]