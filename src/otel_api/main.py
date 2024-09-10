"""Demo FastAPI application with OpenTelemetry instrumentation."""

import logging
import os
import sys
from typing import Any

import httpx
from fastapi import (
    APIRouter,
    FastAPI,
    Request,
    Response,
    status,
)
from opentelemetry import metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

ROUTER = APIRouter(tags=["OTel FastAPI"])

# get log level from environment variable
# LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG").upper()

# configure logger object with the desired log level and format
logging.basicConfig(
    format="{asctime} | {levelname} | {name}:{lineno}:{funcName} | {message}",
    style="{",  # uses {} as placeholders
    # level=LOG_LEVEL,
    stream=sys.stdout,  # where to write the log messages, in this case stdout or console
)

# create logger object with the name of the current module/file to start logging
logger = logging.getLogger(__name__)
meter = metrics.get_meter(__name__)

request_counter = meter.create_counter(name="request_count", description="Request count per endpoint")


# from rich import inspect

async def request_count_metric__middleware(request: Request, call_next):
    
    # inspect(request)
    
    request_counter.add(1, {"method2": request.method, "path2": request.url.path, "query2": "AMIT"})
    # meter.create_counter(name=request.method, unit="Count", description="Request count per endpoint")

    response = await call_next(request)
    return response


class EchoRequestBody(BaseModel):
    message: str


@ROUTER.get("/hello")
async def read_hello(response: Response) -> dict[str, str]:
    response.status_code = status.HTTP_200_OK
    logger.info("Hello, World! is logged")
    return {"message": "Hello, World!"}


@ROUTER.get("/httpbin")
async def httpbin(response: Response) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://httpbin.org/get")
        response.status_code = resp.status_code
        logger.debug("httpbin response: %s", resp.json())
        logger.info("httpbin is successfully called")
        return resp.json()


@ROUTER.post("/echo")
async def echo(body: EchoRequestBody, response: Response) -> dict[str, str]:
    response.status_code = status.HTTP_200_OK
    logger.info("Echoing message: %s", body.message)
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
