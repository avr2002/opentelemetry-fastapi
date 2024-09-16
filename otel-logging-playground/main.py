"""Demo FastAPI application with OpenTelemetry instrumentation."""

import logging
import time
import sys
from logging import Logger
from typing import (
    Any,
)

import httpx
from fastapi import (
    APIRouter,
    FastAPI,
    Request,
    Response,
    status,
)

# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

ROUTER = APIRouter(tags=["OTel FastAPI"])

# get log level from environment variable
# LOG_LEVEL = os.environ["LOG_LEVEL"].upper()
# os.environ.get("LOG_LEVEL", "INFO").upper()

# configure logger object with the desired log level and format
# logging.basicConfig(
#     # format="{asctime} | {levelname} | {name}:{lineno}:{funcName} | {message}",
#     # style="{",  # uses {} as placeholders
#     # level="INFO",  # log level
#     stream=sys.stdout,  # where to write the log messages, in this case stdout or console
# )

# Suppress logs from `httpx` or other external libraries by setting a higher log level for them
# logging.getLogger("httpx").setLevel(logging.WARNING)  # Set this to WARNING or higher to avoid debug/info logs


# create logger object with the name of the current module/file to start logging
logger: Logger = logging.getLogger(__name__)


class EchoRequestBody(BaseModel):
    message: str


@ROUTER.get("/hello")
async def read_hello(response: Response) -> dict[str, str]:
    time.sleep(2)
    logger.info("Sleeping for 2 second before saying Hello, World!")

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


@ROUTER.get("/jsonplaceholder/posts/{post_id}")
async def get_post(post_id: int, response: Response) -> dict[str, Any]:
    """Fetches a list of posts from jsonplaceholder."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
        response.status_code = resp.status_code

        logger.debug("jsonplaceholder response: %s", resp.json())
        logger.info("jsonplaceholder posts fetched successfully")
        return resp.json()


@ROUTER.post("/echo")
async def echo(body: EchoRequestBody, response: Response) -> dict[str, str]:
    response.status_code = status.HTTP_200_OK
    logger.info("Echoing message: %s", body.message)
    return {"message": body.message}


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/")
    app.include_router(ROUTER)

    # FastAPIInstrumentor().instrument_app(app)

    logger.info("Application started")
    # print("HIIIIIIIIIIIIIIIIIIIIIIIII", flush=True)
    # logging.getLogger().info("FastAPI App started")
    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="localhost", port=8000)
