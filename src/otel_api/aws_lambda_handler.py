"""
AWS Lambda handler using Mangum as an ASGI adapter for the FastAPI application.

Repository: https://github.com/jordaneremieff/mangum
"""

from otel_api.main import create_app
from mangum import Mangum

APP = create_app()

handler = Mangum(APP)
