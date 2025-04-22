FROM python:3.11-slim AS base

WORKDIR /app
COPY main.py ./
RUN pip install requests

CMD [ "python", "main.py" ]