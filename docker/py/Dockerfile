FROM python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ../.. .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["watchmedo", "auto-restart", "--recursive", "--directory", ".", "--pattern", "*.py", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]