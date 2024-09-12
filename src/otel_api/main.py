"""Demo FastAPI application with OpenTelemetry instrumentation."""

import logging
import os
import sys
import time
from logging import Logger
from typing import Any

import httpx
from fastapi import (
    APIRouter,
    FastAPI,
    Request,
    Response,
    status,
)
from opentelemetry import (
    metrics,
    trace,
)
from opentelemetry.metrics import Meter
from opentelemetry.trace import Tracer

# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

ROUTER = APIRouter(tags=["OTel FastAPI"])

# get log level from environment variable
LOG_LEVEL = os.environ["LOG_LEVEL"].upper()
# os.environ.get("LOG_LEVEL", "INFO").upper()

# configure logger object with the desired log level and format
logging.basicConfig(
    format="{asctime} | {levelname} | {name}:{lineno}:{funcName} | {message}",
    style="{",  # uses {} as placeholders
    level=LOG_LEVEL,
    stream=sys.stdout,  # where to write the log messages, in this case stdout or console
)

# create logger object with the name of the current module/file to start logging
logger: Logger = logging.getLogger(__name__)
meter: Meter = metrics.get_meter(__name__)
tracer: Tracer = trace.get_tracer(__name__)

request_counter = meter.create_counter(name="RequestCount", description="Request Count per Endpoint")


async def request_count_metric__middleware(request: Request, call_next):
    """Middleware to count the number of requests to each endpoint."""
    request_counter.add(1)
    # meter.create_counter(name=request.method, unit="Count", description="Request count per endpoint")

    response = await call_next(request)
    return response


class EchoRequestBody(BaseModel):
    message: str


@ROUTER.get("/hello")
async def read_hello(response: Response) -> dict[str, str]:
    with tracer.start_as_current_span("sayHelloSpan") as span:
        # Sleep
        with tracer.start_as_current_span("SleepingWhileSayingHelloSpan") as sleep_span:
            time.sleep(2)
            logger.info("Sleeping for 2 second before saying Hello, World!")
            sleep_span.set_attribute("sleep", "2s")

        response.status_code = status.HTTP_200_OK
        logger.info("Hello, World! is logged")

        span.set_attributes(
            {
                "Hello-to": "the-World",
                "Hello-from": "OpenTelemetry",
            }
        )
        return {"message": "Hello, World!"}


@ROUTER.get("/httpbin")
async def httpbin(response: Response) -> dict[str, Any]:
    with tracer.start_as_current_span("httpbinSpan") as span:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://httpbin.org/get")
            response.status_code = resp.status_code

            span.set_attributes(
                {
                    "http.method": "GET",
                    "http.status_code": resp.status_code,
                    "http.url": str(resp.url),
                }
            )
            logger.debug("httpbin response: %s", resp.json())
            logger.info("httpbin is successfully called")
            return resp.json()


@ROUTER.get("/jsonplaceholder/posts/{post_id}")
async def get_post(post_id: int, response: Response) -> dict[str, Any]:
    """Fetches a list of posts from jsonplaceholder."""
    with tracer.start_as_current_span("GetPostsSpan") as span:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
            response.status_code = resp.status_code

            span.set_attributes(
                {
                    "http.method": "GET",
                    "http.status_code": resp.status_code,
                    "http.url": str(resp.url),
                }
            )
            logger.debug("jsonplaceholder response: %s", resp.json())
            logger.info("jsonplaceholder posts fetched successfully")
            return resp.json()


@ROUTER.post("/echo")
async def echo(body: EchoRequestBody, response: Response) -> dict[str, str]:
    with tracer.start_as_current_span("echoSpan") as span:
        response.status_code = status.HTTP_200_OK
        logger.info("Echoing message: %s", body.message)

        span.set_attribute("message", body.message)
        return {"message": body.message}


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/")
    app.include_router(ROUTER)
    app.middleware("http")(request_count_metric__middleware)

    # FastAPIInstrumentor().instrument_app(app)

    logger.info("Application started")
    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="localhost", port=8000)
