FROM python:3.11-slim

WORKDIR /app

# copy/create bare minimum files needed to install dependencies
COPY pyproject.toml /app/
RUN mkdir -p /app/src/otel_api
RUN touch /app/src/otel_api/__init__.py

# install dependencies
RUN pip install --upgrade pip
RUN pip install --editable "/app/[docker]"
RUN opentelemetry-bootstrap --action requirements > /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


# copy the rest of the source code
COPY ./src/ /app/src/
COPY ./tests/ /app/tests/

ENV PORT=8000


# start the server with opentelemetry-instrument
CMD opentelemetry-instrument \
    gunicorn \
    --workers 4 \
    --worker-class "uvicorn.workers.UvicornWorker" \
    --bind "0.0.0.0:$PORT" \
    --reload \
    "otel_api.main:create_app()"