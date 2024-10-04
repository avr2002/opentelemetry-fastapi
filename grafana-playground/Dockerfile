FROM python:3.11-slim

WORKDIR /app

# copy/create bare minimum files needed to install dependencies
COPY requirements.txt /app/requirements.txt
RUN touch /app/__init__.py

# install dependencies
RUN pip install --upgrade pip
# RUN opentelemetry-bootstrap --action requirements >> /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


# copy the rest of the source code
COPY ./main.py /app/main.py

ENV PORT=8000


# start the server with opentelemetry-instrument
# ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
# ENV OTEL_PYTHON_LOGGING_LOGLEVEL=DEBUG
# ENV OTEL_PYTHON_LOG_CORRELATION=true

# ENV OTEL_PYTHON_LOG_CORRELATION=true
# # ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
# ENV OTEL_PYTHON_LOG_LEVEL=debug
# ENV OTEL_PYTHON_LOG_FORMAT="%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s trace_sampled=%(otelTraceSampled)s] - %(message)s"""
      

# --logs_exporter console,otlp \
#     --service_name python-logs-example \

CMD opentelemetry-instrument \
    gunicorn \
    --workers 4 \
    --worker-class "uvicorn.workers.UvicornWorker" \
    --bind "0.0.0.0:$PORT" \
    --reload \
    "main:create_app()"